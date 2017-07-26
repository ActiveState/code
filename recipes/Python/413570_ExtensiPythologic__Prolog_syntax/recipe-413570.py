"""
Here's some changes to the code to add support for pylog. You'll need pylog to run the test. Also, changed the code to use & instead of requiring []. Also added beginings of support for forward chaining. Enjoy! -Huu 

"""
#
# Pythologic.py
#
# Add logic programming (Prolog) syntax into Python.
#
# (c) 2004 Shai Berger
#
import string
from pylog import *


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
        self.prev = None
        self.next = None        
        self.forwardchain_body = None
        self.conditional_body = None
        self.forwardchain_head = None
        self.conditional_head = None
        
    def __pos__(self):
        """
        unary + means insert into database as fact
        """
        self.database.add_fact(self)
        return self

    def __neg__(self):
        """
        unary - means retract from database as fact
        """
        return self

    def __lshift__(self, body):
        """
        The ideal is
        consequent(args) << cond1(args1),...
        for now we must do with
        consequent(args) << (cond1(args1),...)
        """
        self.conditional_body =  body
        body.conditional_head = self
        self.database.add_conditional(self)
        return body


    def __rshift__(self, head):
        """
        create a forward chaining rule.

        """
        head.forwardchain_body = self
        self.forwardchain_head = head
        self.database.add_forwardchain(head)
        return self

    def __rand__(self, other):
        """
        concatenates predicates
        a & b -> c

        """
        if self.forwardchain_head:
            self.prev = other
            other.next = self
            return other
        elif other.conditional_head:
            self.prev = other
            other.next = self
            return self
        else:
            self.prev = other
            other.next = self
            return self

    def __ror__(self, next):
        """
        concatenates predicates
        a & b -> c
        TODO
        """
        print "ror", self, next
        return self

    def __str__(self):
        def tostr(s):
            if isinstance(s, list):
                return "["+string.joinfields(map(str,s), ", ")+"]"
            else:
                return str(s)

        def str_prev(s):
            ret0 = ""
            while s!= None:
                if ret0 == "":
                    ret0 = str(s)
                else:
                    ret0 = str(s) + ", " + ret0                    
                s = s.prev
            return ret0

        def str_next(s):
            ret0 = ""
            while s!= None:
                if ret0 == "":
                    ret0 = str(s)
                else:
                    ret0 = ret0 + ", " + str(s)                    
                s = s.next
            return ret0
        
        subs = map (tostr, self.subs)
        ret = str(self.head) + "(" + string.join(subs,',') + ")"
        if self.forwardchain_body:
            ret = str_prev(self.forwardchain_body) + " -> " + ret
        if self.conditional_body:
            ret = ret + " :- " + str_next(self.conditional_body)
        return ret
        

class Symbol:
    def __init__ (self, name, database):
        self.name = name
        self.database = database
    def __call__ (self, *args):
        return Struct(self.database, self, args)
    def __str__(self):
        return self.name

class Constant(Symbol):
    """
    A constant is a name. Its value is its name too.
    """
    def value(self): return self.name

class Variable(Symbol):
    def __str__(self):
#        return "?"+self.name
        return self.name


def symbol(name, database):
    if (name[0] in string.uppercase):
        return Variable(name,database)
    else:
        return Constant(name, database)

class Database:
    def __init__(self):
        self.facts = []
        self.conditionals = []
        self.forwardchain = []        
    def add_fact(self, fact):
        self.facts.append(fact)
    def add_conditional(self,head):
        self.conditionals.append(head)
    def add_forwardchain(self,head):
        self.forwardchain.append(head)

    def prt(self):
        """
        Print the database in somewhat readable (prolog) form
        """
        for f in self.facts: print f, "."
        for f in self.forwardchain: print f, "."
        for f in self.conditionals: print f, "."


    def compile(self):
        # do pylog's compile
        exec compile(self.__str__()) in globals()


    def __str__(self):
        ret = ""
        for f in self.facts: ret += str(f) +  ".\n"
        for f in self.conditionals: ret += str(f) +  ".\n"
#       forward chaining not yet supported
#        for f in self.forwardchain: ret += str(f) +  ".\n"                
        return ret
        
    def consult(self, func):
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
        # Python < 2.0
        # undefined = filter (lambda n,d=defined: n not in d, names)
        # Modern Python
        undefined = [name for name in names if name not in defined]
        # Generate the new global environment for the function;
        # to the old environment, add definitions for all undefined
        # symbols, which relate to this database (self). When the
        # symbols are operated on in the function, they will add
        # facts and conditionals to the database.
        newglobals = func.func_globals.copy()
        for name in undefined:
            newglobals[name] = symbol(name, self)
        exec code in newglobals
        

    def consult_and_transform(self, func):
        """
        A helper for decorator implementation
        """
        self.consult(func)
        return LogicalFunction(self, func)

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

def logical(database):
    """
    A decorator for logical functions
    """
    return database.consult_and_transform

class Test:
    db = Database()

    @logical(db)
    def _rules():
        likes('sam',Food) << indian(Food) & mild(Food)
        likes('sam',Food) << chinese(Food)
        likes('sam',Food) << italian(Food)
        likes('sam','chips')

        +indian('curry')
        +indian('dahl')
        +indian('tandoori')
        +indian('kurma')

        +mild('dahl')
        +mild('tandoori')
        +mild('kurma')

        +chinese('chow_mein')
        +chinese('chop_suey')
        +chinese('sweet_and_sour')

        +italian('pizza')
        +italian('spaghetti')


    def __init__(self):
        self.db.prt()
        self.db.compile()
    
    def test(self):
        WHO, WHAT = Var('WHO'), Var('WHAT')
        queries =	[
            likes('sam','dahl'),
            likes('sam','chop_suey'),
            likes('sam','pizza'),
            likes('sam','chips'),
            likes('sam','curry'),
            likes(WHO,WHAT),
                                ]

        for query in queries:
                print "?", query
                n=0
                for _ in query():
                        print "\tyes:", query
                        n += 1
                if n==0:
                        print "\tno"
        
if __name__ == "__main__":

    test = Test()
    test.test()
