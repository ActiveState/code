"""A wrapper around DBAPI-compliant databases to support iteration
and generator expression syntax for requests, instead of SQL

To get an iterator, initialize a connection to the database, then
set the cursor attribute of the query class to its cursor

Create an instance of Table for the tables you want to use

Then you can use the class query. You create an instance by passing
a generator expression as parameter. This instance translates the
generator expression in an SQL statement ; then you can iterate
on it to get the selected items as objects, dictionaries or lists

Supposing you call this module db_iterator.py, here is an example 
of use with sqlite :

    from pysqlite2 import dbapi2 as sqlite
    from db_iterator import query, Table

    conn = sqlite.connect('planes')
    query.cursor = conn.cursor()

    plane = Table()
    countries = Table()

    # all the items produced by iteration on query() are instances
    # of the Record class
    
    # simple requests
    # since no attribute of r is specified in the query, returns a list
    # of instances of Record with attributes matching all the field names
    print [ r.name for r in query(r for r in plane if r.country == 'France') ]
    
    # this request returns a list instances of Record with the attribute 
    # c_country (c.country with the . replaced by _)
    print [ country for country in query(c.country for c in countries 
            if c.continent == 'Europe') ]

    # request on two tables
    print [r.name for r in query (r for r in plane for c in countries 
            if r.country == c.country and c.continent == 'Europe')]

"""
import tokenize
import token
import compiler
import types

class ge_visitor:
    """Instances of ge_visitor are used as the visitor argument to 
    compiler.walk(tree,visitor) where tree is an AST tree built by
    compiler.parse
    The instance has a src attribute which looks like the source
    code from which the tree was built
    Only a few of the visitNodeType are implemented, those likely to appear
    in a database query. Can be easily extended
    """

    def __init__(self):
        self.src = ''

    def visitTuple(self,t):
        self.src += ','.join ( [ get_source(n) for n in t.nodes ])

    def visitList(self,t):
        self.src += ','.join ( [ get_source(n) for n in t.nodes ])

    def visitMul(self,t):
        self.src += '(%s)' %('*'.join([ get_source(n) for n in t]))

    def visitName(self,t):
        self.src += t.name

    def visitConst(self,t):
        if type(t.value) is str:
            # convert single quotes, SQL-style
            self.src += "'%s'" %t.value.replace("'","''")
        else:
            self.src += str(t.value)

    def visitAssName(self,t):
        self.src += t.name

    def visitGetattr(self,t):
        self.src += '%s.%s' %(get_source(t.expr),str(t.attrname))

    def visitGenExprFor(self,t):
        self.src += 'for %s in %s ' %(get_source(t.assign),
                get_source(t.iter))
        if t.ifs:
            self.src += ' if ' +''.join([ get_source(i) for i in t.ifs ])

    def visitGenExprIf(self,t):
        self.src += get_source(t.test)

    def visitCompare(self,t):
        compiler.walk(t.expr,self)
        self.src += ' '
        for o in t.ops:
            oper = o[0]
            if oper == '==':
                oper = '='
            self.src += oper + ' '
            compiler.walk(o[1],self)

    def visitAnd(self,t):
        self.src += '('
        self.src += ' AND '.join([ get_source(n) for n in t.nodes ])
        self.src+= ')'

    def visitOr(self,t):
        self.src += '('
        self.src += ' OR '.join([ get_source(n) for n in t.nodes ])
        self.src+= ')'

    def visitNot(self,t):
        self.src += '(NOT ' + get_source(t.expr) + ')'

def get_source(node):
    """Return the source code of the node, built by an instance of
    ge_visitor"""
    return compiler.walk(node,ge_visitor()).src

class genExprVisitor:
    """Visitor used to initialize GeneratorExpression objects
    Uses the visitor pattern. See the compiler.visitor module"""

    def __init__(self):
        self.GenExprs = []

    def visitGenExprInner(self,node):
        ge = GeneratorExpression()
        self.GenExprs.append(ge)
        for y in node.getChildren():
            if y.__class__ is compiler.ast.GenExprFor:
                ge.exprfor.append(y)
            else:
                ge.result = y

class GeneratorExpression:
    """A class for a Generator Expression"""
    def __init__(self):
        self.result = None
        self.exprfor = []
        
class Record(object):
    """A generic class for database records"""
    pass

class Table:
    """A basic iterable class to avoid syntax errors"""
    def __iter__(self):
        return self
    
class query:
    """Class used for database queries
    Instance is created with query(ge) where ge is a generator
    expression
    The __init__ method builds the SQL select expression matching the
    generator expression
    Iteration on the instance of query yields the items found by
    the SQL select, under the form specified by return_type : an object,
    a dictionary or a list"""

    cursor = None   # to be set to the cursor of the connection
    return_type = object    # can be set to dict or list

    def __init__(self,s):
        self._iterating = False # used in next()

        # First we must get the source code of the generator expression
        # I use an ugly hack with stack frame attributes and tokenize
        # If there's a cleaner and safer way, please tell me !
        readline = open(s.gi_frame.f_code.co_filename).readline
        first_line = s.gi_frame.f_code.co_firstlineno
        flag = False
        self.source = ''    # the source code
        for t in tokenize.generate_tokens(open(s.gi_frame.f_code.co_filename).readline):
            # check all tokens until the last parenthesis is closed
            t_type,t_string,(r_start,c_start),(r_end,c_end),line = t
            t_name = token.tok_name[t_type]
            if r_start == first_line:
                if t_name == 'NAME' and t_string=="query":
                    flag = True
                    res = t_string
                    start = 0 # number of parenthesis
                    continue
            if flag:
                self.source += ' '+t_string
                if t_name == 'OP':
                        if t_string=='(':
                            start += 1
                        elif t_string == ')':
                            start -= 1
                            if start == 0:
                                break
        # when the source has been found, build an AST tree from it
        ast = compiler.parse(self.source.strip())
        # use a visitor to find the generator expression(s) in the source
        visitor = genExprVisitor()
        compiler.walk(ast,visitor)
        # if there are nested generator expressions, it's too difficult
        # to handle : raise an exception
        if len(visitor.GenExprs)>1:
            raise Exception,'Invalid expression, found more ' \
                'than 1 generator expression'
        ge = visitor.GenExprs[0]
        self.sql = self.build_sql(ge)

    def build_sql(self,ge):
        """ Build the SQL select for the generator expression
        ge is an instance of GeneratorExpression
        The generator expression looks like
        (result) for x1 in table1 [ for x2 in table2] [ if condition ]
        It has 2 attributes :
        - result : an AST tree with the "result" part
        - exprfor : a list of AST trees, one for each "for ... in ..."
        """
        self.res = []
        if ge.result.__class__ is compiler.ast.Tuple:
            # more than one item in result
            self.res = ge.result.getChildren()
        else:
            self.res = [ge.result]
        results = [] # a list of strings = result part of the SQL expression
        for res in self.res:
            # a result can be a stand-alone name, or a "qualified" name,
            # with the table name first (table.field)
            if res.__class__ is compiler.ast.Name:
                results.append((res.name,None))
            elif res.__class__ is compiler.ast.Getattr:
                results.append((get_source(res.expr),res.attrname))
        self.results = results

        # "for x in y" produces an item in the dictionary recdefs :
        # recdef[x] = y
        recdefs = {}
        conditions = []
        for exprfor in ge.exprfor:
            recdefs[get_source(exprfor.assign)] = \
                get_source(exprfor.iter)
            if exprfor.ifs:
                # an AST tree for the condition
                conditions = exprfor.ifs

        # To build objects or dictionaries in the result set, we must
        # know the name of the fields in all the tables used in the
        # query. For this, make a simple select in each table and read
        # the information in cursor.description
        self.names={}
        for rec,table in recdefs.iteritems():
            self.cursor.execute('SELECT * FROM %s' %table)
            self.names[rec] = [ d[0] for d in self.cursor.description ]

        sql_res = [] # the way the field will appear in the SQL string
        rec_fields = [] # the name of the fields in the object or dictionary
        for (n1,n2) in results:
            if n2 is None:
                # "stand-alone" name
                if n1 in recdefs.keys():
                    sql_res += [ '%s.%s' %(n1,v) for v in self.names[n1] ]
                    rec_fields+=[ v for v in self.names[n1] ]
                else:
                    sql_res.append(n1)
                    rec_fields.append(n1)
            else:
                # "qualified" name, with the table name first
                sql_res.append('%s.%s' %(n1,n2))
                # in the result set, the object will have the attribute 
                # table_name (we can't set an attribute table.name, and
                # name alone could be ambiguous
                rec_fields.append('%s_%s' %(n1,n2))
        self.rec_fields = rec_fields
        
        # now we can build the actual SQL string
        sql = 'SELECT '+ ','.join(sql_res)
        sql += ' FROM '
        froms = []
        for (k,v) in recdefs.iteritems():
            froms.append('%s AS %s ' %(v,k))
        sql += ','.join(froms)
        if conditions:
            sql += 'WHERE '
        for c in conditions:
            sql += get_source(c)

        return sql
            
    def __iter__(self):
        return self
    
    def next(self):
        if not self._iterating:
            # begin iteration
            self.cursor.execute(self.sql)
            self._iterating = True
        row = self.cursor.fetchone()
        if row is not None:
            if self.return_type == object:
                # transform list into instance of Record
                # uses the rec_fields computed in build_sql()
                rec = Record()
                rec.__dict__ = dict(zip(self.rec_fields,row))
                return rec
            elif self.return_type == dict:
                return dict(zip(self.rec_fields,row))
            elif self.return_type == list:
                return row
        self._iterating = False
        raise StopIteration
