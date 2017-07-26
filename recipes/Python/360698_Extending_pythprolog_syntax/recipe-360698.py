#
# pythologic2.py
#
# Add logic programming (Prolog) syntax and *resolution* into Python.
# 
# (c) 2004 Francisco Coelho
# after (c) 2004 Shai Berger
# and AIMA examples
#

import string
import copy
 
class Struct:
    def __init__(self, database, head, subs):
        """
        The head and subs are essential - what makes this struct.
        The database should only be used while structs are constructed,
        and later removed.
        """
        self.database = database
        self.head = head
        self.subs = subs

    def __pos__(self):
        """
        unary + means insert into database as fact
        """
        self.database.add_fact(self)

    def __invert__(self):
        """
        unary ~ means insert into database as query
        """
        self.database.add_query(self)

    def __lshift__(self, requisites):
        """
        The ideal is
        consequent(args) << cond1(args1),...
        for now we must do with
        consequent(args) << [cond1(args1),...]
        """
        self.database.add_conditional(self, requisites)

    def __str__(self):
        subs = map (str, self.subs)
        return str(self.head) + "(" + string.join(subs,',') + ")"

class Symbol:
    def __init__ (self, name, database):
        self.name = name
        self.database = database
            
    def __call__(self, *args):
        return Struct(self.database, self, args)
            
    def __str__(self):
        return self.name

class Constant(Symbol):
    """
    A constant is a name. Its value is its name too.
    """
    def value(self): return self.name

class Variable(Symbol):
    pass


def symbol(name, database):
    if (name[0] in string.uppercase):
        return Variable(name,database)
    else:
        return Constant(name, database)
	
class Database:
    def __init__(self, name):
        self.name= name
        self.facts = []
        self.conditionals = []
        self.queries = []
            
    def add_fact(self, fact):
        self.facts.append(fact)

    def add_query(self, query):
        self.queries.append(query)
            
    def add_conditional(self,head,requisites):
        if not(isinstance(requisites, list)):
            requisites = [requisites]
        self.conditionals.append((head,requisites))

    def __str__(self):
        factsStr= string.join(map(str, self.facts),'\n')
        condsStr= ''
        for (h,r) in self.conditionals:
            condsStr = condsStr +  "%s << %s\n"%(h,string.join( map(str, r), ', '))
        queryStr= string.join( map(str, self.queries),'\n')
        return self.name + ' facts\n' + factsStr +'\n'+self.name + ' conditionals\n'+ condsStr  + '\n'+self.name + ' queries\n'+queryStr + '\n'

    def append(self, func):
        """
        Include definitions from func into database
        """
        try:
            code = func.func_code
        except:
            raise TypeError, "function or method argument expected"
        names = code.co_names
        locally_defined = code.co_varnames
        globally_defined = func.func_globals.keys()
        defined = locally_defined+tuple(globally_defined)
        undefined = [name for name in names if name not in defined]
        newglobals = func.func_globals.copy()
        for name in undefined:
            newglobals[name] = symbol(name, self)
        exec code in newglobals

    def __lshift__(self, func):
        """
        A helper for decorator implementation
        """
        self.append(func)
        return LogicalFunction(self, func)		
            
    def solve(self, V = [{}]):
        """        
        The query queue is LIFO:
        Extend valuations in V satisfying the last query.
        """
        def solve1( v ):
            # get solutions from facts
            unify_facts = [unify(query, fact, v) for fact in self.facts]

            # look for solutions from conditionals
            unify_conditionals = []            
            for ( header , condition_list ) in self.conditionals:
                u = unify(query, header , v) # unify headers
                U = [ u ]
                
                if u != None:
                    # remember query queue
                    oldQueries = copy.deepcopy(self.queries)

                    # we want to start by the first conditional
                    D = copy.copy( condition_list )
                    D.reverse() 
                    
                    # phase 1: append the conditionals to query queue
                    for condition in D:
                        if type( condition ) == type('string'):
                            # process python code
                            # should return True or False
                            self.queries.append( condition )
                            #eval_python_string( condition , u)
                        else:
                            # append the conditional,
                            # with variables replaced according to u
                            # to the query queue
                            unified_condition = subst(u, condition )
                            self.queries.append( unified_condition )

                    # phase 2: solve the appended conditionals
                    for condition in D:
                        U =  self.solve( U )

                    # restore query queue    
                    self.queries = oldQueries

                    # grow the list of solutions
                    unify_conditionals = unify_conditionals + U
            return [ u for u in (unify_facts + unify_conditionals) if not u in [None, {}] ] 
        
        if self.queries:
            query = self.queries[-1]
            del self.queries[-1]
        else:
            return []

        if type( query ) == type( 'string' ):
            U = [ v for v in V if python_eval_string(query, v) ]                    
        else:
            U = []
            
            for v in V:
                U = U + solve1(v)
            
        return U
                    
def python_eval_string(s, v):
    for k in v:
        s=string.replace(s, str(k), str(v[k]))
    return eval( s, {} )

def subst(v, x):
    if v.has_key(x):
        return v[x]
    elif isinstance(x, Variable):
        return x
    elif isinstance(x, Struct):
        return Struct( x.database, x.head, [subst(v, xi) for xi in x.subs])

def unify(x,y,v={}):
    """
    Find one valuation extending v and unifying x with y
    """
    
    def extend(v, x, t):
        """
        Extend valuation v with v[x] = t
        """
        v1 = copy.copy(v)
        v1[x] = t
        return v1

    def occur_check(x, t):
        """
        Test if the variable x occurr in structure t
        """
        if x == t:
            return True
        elif isinstance(t, Struct):
            return t.head == x.head or occur_check(x, t.subs)
        return False

    def unify_var(x, t, v):
        """
        Test if v can be extended with v[x] = t;
        In that case return the extention
        Else return None
        """
        if x in v:
            return unify( v[ x ], t, v)
        elif occur_check(x, t):
            return None
        else:
            return extend(v, x, t)

    if v == None:
        return None
    elif x == y:
        return v
    elif isinstance(x, Variable):
        return unify_var(x, y, v)
    elif isinstance(y, Variable):
        return unify_var(y, x, v)
    elif isinstance(x, Struct) and isinstance(y, Struct) and (x.head == y.head):
        z = v
        n = len(x.subs)
        m = len(y.subs)
        if n == m:
            for i in range( n ):
                z = unify( x.subs[i], y.subs[i], z)
            return z
        else:
            return None
    else:
        return None

    
class LogicalFunction:
    """
    This class replaces a logical function once it has
    been consulted, to avoid erroneous use
    """
    def __init__(self, database, func):
        self.database=database
        self.logical_function=func
    def __call__(self):
        raise TypeError, "Logical functions are not really callable"

if __name__ == "__main__":

    db = Database('TEST')

    print "Defining a prolog program... ",

    def prolog_func():
        
        # prolog facts are prefixed with "+"
        + number(0) 
        + number(1)
        + number(2)
        + number(3)
        + number(4)

        # prolog conditionals have the pattern p << [q1, ..., qn]
        test(X, Y) << [number(X),  number(Y), 'X==2*Y' ]
        
        # prolog queries are prefixed with "~"
        ~ test(X, Y)
        
    # Update the database
    db << prolog_func
    print "done"

    print "Before solving"
    print db
    
    # Solve the queries
    x = db.solve()
    print 'Solutions'
    for v in x:
        for k in v: print k,"=", v[k],' ',
        print

    print "After solving"
    print db
