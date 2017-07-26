#
# Pythologic.py
#
# Add logic programming (Prolog) syntax into Python.
#
# (c) 2004 Shai Berger
#
import string

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

    def __lshift__(self, requisites):
        """
        The ideal is
        consequent(args) << cond1(args1),...
        for now we must do with
        consequent(args) << (cond1(args1),...)
        """
        self.database.add_conditional(self, requisites)

    def __str__(self):
        subs = map (str, self.subs)
        return str(self.head) + "(" + string.join(subs,',') + ")"

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
        return "?"+self.name


def symbol(name, database):
    if (name[0] in string.uppercase):
        return Variable(name,database)
    else:
        return Constant(name, database)

class Database:
    def __init__(self):
        self.facts = []
        self.conditionals = []
    def add_fact(self, fact):
        self.facts.append(fact)
    def add_conditional(self,head,requisites):
        # Older Python
        # if not(isinstance(requisites, type([]))):
        # More modern
        if not(isinstance(requisites, list)):
            requisites = [requisites]
        self.conditionals.append((head,requisites))

    def prt(self):
        """
        Print the database in somewhat readable (prolog) form
        """
        for f in self.facts: print f, "."
        for (h,r) in self.conditionals:
            print h, ":-", string.join(map(str,r), " , "), "."

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

if __name__ == "__main__":

    db = Database()
    global_var = ["known", "fact"]

    print "Defining a logical function...",

    @logical(db)
    def prolog_func():
        # Undefined names are given logical meaning.
        #
        # Following Prolog, if the name starts with an uppercase letter,
        # it is a logical variable (will be printed with a prefixed "?"
        # to clarify), otherwise it is a logical constant.
        #
        # unary plus defines a fact
        + farmer(moshe)
        + donkey(eeyore)
        # left-shift defines a conditional (this is an encoding
        # of the famous "donkey sentence" studied a lot in natural
        # language semantics: "If a farmer has a donkey, he beats it").
        beats(X,Y) << [ farmer(X), donkey(Y), owns(X,Y) ]
        # Define local variables -- regular Python
        x = "'local value of x'"; y = 17
        # Local and global variables (as well as other expressions)
        # can participate in facts and conditionals
        + globally(global_var)
        equal("x","y") << equal(x,y)

    # For Pre-2.4, replace the @logical decorator with this line:
    # prolog_func = db.consult_and_transform(prolog_func)
    print "Done."
    print "Definition has already updated the database as follows:"
    print
    db.prt()
    print
    print "Trying to call the logical function raises an error:"
    print
    prolog_func()
