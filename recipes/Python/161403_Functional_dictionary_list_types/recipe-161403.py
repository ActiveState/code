# ftypes.py - Functional dictionary and list types for Python 2.1+
#
# Author:  Dave Benjamin <ramen@ramenfest.com>
# Version: 1.1.2

"""
Introduction
------------

The purpose of this module is to provide a dictionary and list type that can
aid in relational algebra, functional programming, list-oriented programming,
and perhaps even code obfuscation.

There is a certain dark side to this library: operator overloading. Almost
all of the useful features of these types are invoked through operators. My
rationale is that certain functional/relational methods have become so well-
known that they deserve to be liberated from the highly syntactic domain of
functions to the free and flowy rivers of infix notation. You may disagree.

Part of my inspiration for these ideas came from the late computer scientist
and mathematician Edsger Wybe Dijkstra (11 May 1930 -- 6 August 2002), who
argued that programs should be based on mathematical logic and methodology.
Throughout the process of learning about functional programming techniques,
I began to see the resemblence between pure mathematics and functional
algorithms, and wanted to follow this train of thought further.

The "map" function, for example, is so common and useful (to me, anyway)
that there ought to be a symbolic notation for it. Instead of always having
to write "map(func, list)", perhaps it should be "list MAP func", where "MAP"
could be substituted with the "M"-looking Greek letter of your choice. =)
In fear of accidently reinventing APL, I tried to ignore the temptation to
create such an operator in Python, but it seemed so logical and natural
after awhile that I really wanted to try it in practice.

As you will see, I have indeed implemented map as an operator (*), as well
as filter (/), reduce (()), sort (%), zip (**), and many other common
FP-related functions. As is usually the case with liberal operator
overloading, the choice in operator symbols is somewhat arbitrary. I am
reasonably happy with my choices so far, but I did not reach this without
sometimes painful self-deliberation.

Another factor that contributed to this code was a need for powerful tools
to deal with result sets from database queries. My "discovery" that result
sets could be mapped to lists of dictionaries was somewhat of an epiphany,
and enabled me to find very concise solutions to common database and web
templating problems. Not only can dictionaries represent database rows, but
they also function as namespaces for template evaluation.

Defining a result set (or, more formally, a "relation") as a list of
dictionaries allowed me to apply these types to the domain of relational
algebra: operators such as select (which is essentially the same operation
as filter), project (also implemented using the / operator), distinct
(implemented using the unary -), and union (+, merely list concatenation)
fit nicely into this list/dictionary model. The list constructor is
extended to allow for concise specification of literal result sets as
follows:

list(['id', 'fname', 'lname'     ],
     #---------------------------#
     [1234, 'Guido', 'van Rossum'],
     [1235, 'Alex',  'Martelli'  ],
     [1236, 'Tim',   'Peters'    ])

This constructor will return a list of three dictionaries, each containing
the keys "id", "fname", and "lname", pointing to the respective values for
each of the rows above. Since most database APIs can provide results in this
form, literal and actual result sets can be swapped freely. As a result,
you can test database code without the database, even through the interpreter
if you desire. This has been very useful.

The examples below should demonstrate the usage of the aforementioned
features, plus many others. You may wish to consult the code itself for
more ideas about how to use these types.

How-To
------

Import these types:
    from ftypes import *

Import these types without overwriting the original ones:
    from ftypes import list as flist, dict as fdict

Instantiate these types:
    dict()                                    -> {}
    dict({'a': 5, 'b': 6})                    -> {'b': 6, 'a': 5}
    dict(((1, 2), (3, 4)))                    -> {3: 4, 1: 2}
    dict(('a', 'b', 'c'), (1, 2, 3))          -> {'b': 2, 'c': 3, 'a': 1}
    list()                                    -> []
    list([1, 2, 3])                           -> [1, 2, 3]
 ++ list(['st', 'state'        ],
         ['AZ', 'Arizona'      ],
         ['CA', 'California'   ],
         ['PZ', 'Planet Zektar']) -> [{'st': 'AZ', 'state': 'Arizona'},
                                      {'st': 'CA', 'state': 'California'},
                                      {'st': 'PZ', 'state': 'Planet Zektar'}]
Do functional things:
    list([1, 3, 5, 7]) * (lambda x: x + 1)    -> [2, 4, 6, 8] (map)
    list([2, 3, 4, 5]) / (lambda x: x % 2)    -> [3, 5] (filter)
    list(range(5)).reduce(operator.add)       -> 10 (reduce)
    list('abcde') % (lambda x, y: cmp(y, x))  -> ['e','d','c','b','a'] (sort)
    list([0, '0', [], '[]']) / operator.truth -> ['0', '[]'] (any)
    list([1, 2, 3]) ** [4, 5, 6]              -> [[1, 4], [2, 5], [3, 6]] (zip)
    
    The map (*) and filter (/) operators are also available for the dict type.
    The given function will be applied to the dictionary's values.

Do relational things:
    states.st                                 -> ['AZ', 'CA', 'PZ'] (column)
    (states / (lambda x: x.st != 'CA')).st    -> ['AZ', 'PZ'] (select)
    (states / ['st'])                         -> [{'st': 'AZ'},
                                                  {'st': 'CA'},
                                                  {'st': 'PZ'}] (project)
    -list([1, 2, 2, 3, 6, 3, 2])              -> [1, 2, 3, 6] (distinct)
                                                  
    Note: The definition of states can be found above as indicated (++).
 
Other (maybe) useful tricks:    
    list([1, 2, 3]) / {1: 1, 3: 1}.has_key    -> [1, 3] (dict set filter)
    dict({'a': 5, 'b': 6}).a                  -> 5 (object-style dict lookup)
    dict({'a': 5, 'b': 6}.items())            -> {'b': 6, 'a': 5} (identity)
    dict({'a': 5, 'b': 6}).items() * list     -> [['b', 6], ['a', 5]] (cast)
    ~list([(1, 2), (3, 4)])                   -> [[1, 3], [2, 4]] (transpose)
    ~dict({1: 2, 3: 4})                       -> {2: 1, 4: 3} (dict transpose)
    dict().set('a', 5).set('b', 6).unset('a') -> {'b': 6} (mutator chaining)
    d = dict(); (5 + d.put('a', 6 + 7)) * d.a -> 234 (memoization)
    list(range(5)) * list(range(4)).get       -> [0, 1, 2, 3, None] (list get)
    list(['hello', 'world']).join(' ')        -> 'hello world' (string join)
    dict({'a': 5, 'b': 6}).eval('a + b')      -> 11 (eval within a namespace)

Callables:
    Dictionaries and lists can be made callable, ie. they can be invoked
    like functions. This behavior can be activated by supplying the named
    parameter "__call__" to the constructors. For example:
    
    list([1,2,3], __call__=list.reduce)(operator.add) -> 6
    
    I believe that this fits the definition of a "closure".
    
    The ability to add methods via keyword arguments is not restricted to
    __call__, by the way. You can in fact supply any method you would like
    to override as a keyword argument to the dict and list constructors.

Sets and Histograms:
    As a matter of convience, set and constructor functions have been
    provided, both returning dictionaries.
    
    Use set(1, 2, 3) as an alternative to dict({1: 1, 2: 1, 3: 1}).
    To convert a list "liszt" to a set, write set(*liszt). The binary
    operators &, |, and - have been overridden to function as set
    intersection, union, and difference, respectively. The "in"
    operator is an alias for has_key, as with more recent versions of
    Python's built-in dictionary, so it can be used to test for set
    containment.
    
    The histogram function counts the number of occurrences (frequency) of
    each element in a list. It takes a single list as its argument (unlike
    set(), which accepts a variable number of arguments) and returns a
    dictionary where the list elements are the keys and their values are
    their respective frequency counts.
    
    Both of these constructors deal only with hashable types. They will
    pass on any named parameters to dict().
    
Afterword
---------

Thanks to Guido for such a powerful and flexible language! I welcome any
ideas, contributions, and criticism from the community. Thanks also to
Alex Martelli for the fantastic "curry" implementation on ActiveState's
Python Cookbook, and to Tim Peters for starting the helpful discussion on
extracting unique elements from a list.

Peace!
Dave Benjamin <ramen@ramenfest.com>
"""

from __future__ import nested_scopes
from UserDict   import UserDict
from UserList   import UserList
from pprint     import pformat

__all__ = ['dict', 'list', 'odict', 'oset', 'set']

# List Class
# ----------

class list(UserList):
    def __init__(self, *args, **kwds):
        # Import keyword arguments into the object dictionary.
        # Callables are automatically curried so that they take
        # "self" as the first argument".
        for key, val in kwds.items():
            if callable(val):
                self.__dict__[key] = curry(val, self)
            else:
                self.__dict__[key] = val

        if len(args) == 0:
            # No arguments: empty list.
            UserList.__init__(self)

        elif len(args) == 1:
            # One argument: list.
            UserList.__init__(self, args[0])

        else:
            # Two arguments: list of dictionaries.
            UserList.__init__(self, [dict(args[0], row) for row in args[1:]])

    def copy(self):
        """Copy constructor."""
        return self[:]
    
    def column(self, key):
        """Get column."""
        return list([item[key] for item in self])

    def flip(self):
        """Convert list of dictionaries to dictionary of lists."""
        result = dict()
        if not self: return result
        for key in self[0].keys():
            result[key] = self.column(key)
        return result

    def get(self, idx, default=None):
        """Get item."""
        try:
            return self.data[idx]
        except IndexError:
            return default

    def join(self, sep=''):
        """String join with reversed semantics."""
        return sep.join(self)

    def reduce(self, func, *initial):
        """Reduce to a single value by iteratively applying a function."""
        if initial: return reduce(func, self, initial[0])
        return reduce(func, self)

    def __mul__(self, func_or_n):
        """Map/repeat (*)."""
        
        if callable(func_or_n):
            # Function: map operation.
            return list([func_or_n(x) for x in self])
            
        else:
            # Number: repeat operation.
            return list(self.data * func_or_n)

    def __div__(self, func_or_keys):
        """Filter/select/project (/)."""
        
        if callable(func_or_keys):
            # Function: select (filter) operation.
            return list([x for x in self if func_or_keys(x)])
        
        else:
            # Key list: project operation.
            return list([dict(x) / func_or_keys for x in self])

    def __mod__(self, func):
        """Sort (%)."""
        result = self[:]
        result.sort(func)
        return result

    def __pow__(self, other):
        """Zip (**)."""
        return list(zip(self, other)) * list

    def __invert__(self):
        """Transpose (~)."""
        if not self: return list()
        return list(zip(*self)) * list

    def __neg__(self):
        """Distinct (unary -)."""
        result = list()
        
        try:
            # Hash method (faster).
            seen = dict()
            for item in self:
                if item not in seen:
                    seen[item] = 1
                    result.append(item)
            
        except TypeError:
            # Linear method (more compatible).
            for item in self:
                if item not in result:
                    result.append(item)
                    
        return result

    def __getattr__(self, key):
        """Get column or attribute (.)."""

        if key == '__methods__':
            return UserList.__dict__.keys()

        if key == '__members__':
            if self.data and hasattr(self.data[0], 'keys'):
                return self.data[0].keys()
            else:
                return []

        if self.__dict__.has_key(key):
            return self.__dict__[key]

        if self.data:
            head = self.data[0]
            if hasattr(head, 'has_key') and head.has_key(key):
                return self.column(key)
            #if hasattr(head, key):
            if hasattr(head, '__dict__') and head.__dict__.has_key(key):
                return list([getattr(x, key) for x in self])
        
        raise AttributeError, key
    
    def __str__(self):
        """Built-in pretty-printer."""
        return pformat(self.data)

# Dictionary Class
# ----------------

class dict(UserDict):
    def __init__(self, *args, **kwds):
        # Import keyword arguments into the object dictionary.
        # Callables are automatically curried so that they take
        # "self" as the first argument".
        for key, val in kwds.items():
            if callable(val):
                self.__dict__[key] = curry(val, self)
            else:
                self.__dict__[key] = val
            
        if len(args) == 0:
            # No arguments: empty dictionary.
            UserDict.__init__(self)
        
        elif len(args) == 1:
            # One argument: dictionary or item list.
            
            if hasattr(args[0], 'items'):
                # Dictionary.
                UserDict.__init__(self, args[0])
                
            else:
                # Item list.
                UserDict.__init__(self)
                for key, val in args[0]:
                    self[key] = val
        else:
            # Two arguments: key and value lists.
            UserDict.__init__(self)
            for key, val in zip(args[0], args[1]):
                self[key] = val

    def copy(self):
        """Copy constructor."""
        return dict(self.data)
    
    def keys(self):
        """Returns keys as overloaded list."""
        return list(self.data.keys())
    
    def values(self):
        """Returns values as overloaded list."""
        return list(self.data.values())
    
    def items(self):
        """Returns items as overloaded lists of tuples."""
        return list(self.data.items())
    
    def eval(self, expr, vars={}):
        """Evaluate an expression using self as the namespace (())."""
        return eval(expr, self.data, vars)
        
    def flip(self):
        """Convert dictionary of lists to list of dictionaries."""
        return list(self.keys(), *~self.values())
    
    def set(self, key, val=1):
        """Assignment as method. Returns self."""
        self[key] = val
        return self

    def unset(self, key):
        """Deletion as method. Returns self."""
        del self[key]
        return self
    
    def put(self, key, val):
        """Assignment as method. Returns the assigned value."""
        self[key] = val
        return val
    
    def __and__(self, other):
        """Intersection (&)."""
        result = dict()
        for key in self.keys():
            if other.has_key(key):
                result[key] = self[key]
        return result

    def __or__(self, other):
        """Union (|)."""
        result = dict(self.data)
        result.update(other)
        return result

    def __add__(self, other):
        """
        Merge (+).
        
        The merge operation is similar to a union except that data is
        never overwritten. If three dictionaries with the same set of
        keys are merged, the resulting dictionary's values will be
        three-element lists.
        
        If you want destructive behavior, use the union (|) operator
        instead, since it pays no consideration to duplicate keys.
        """
        result = dict(self.data)
        
        for key in other.keys():
            if result.has_key(key):
                if hasattr(result[key], 'append'):
                    result[key].append(other[key])
                else:
                    result[key] = list([result[key], other[key]])
            else:
                result[key] = other[key]
                
        return result
    
    def __sub__(self, other):
        """Difference (-)."""
        
        result = dict()
        
        for key in self.keys():
            if not other.has_key(key):
                result[key] = self[key]
                
        return result
    
    def __mul__(self, func_or_n):
        """Map/repeat (*)."""
        
        result = dict()
        
        if callable(func_or_n):
            for key in self.keys():
                result[key] = func_or_n(key, self[key])
        else:
            for key in self.keys():
                result[key] = list([self[key]]) * func_or_n
                
        return result
    
    def __div__(self, func_or_keys):
        """Filter/extract (/)."""
        
        result = dict()
        
        if callable(func_or_keys):
            for key in self.keys():
                if func_or_keys(key, self[key]):
                    result[key] = self[key]
        else:
            for key in func_or_keys:
                result[key] = self[key]
                
        return result

    def __pow__(self, other):
        """Compose (**)."""
        result = dict()
        for key in self.keys():
            result[key] = other[self[key]]
        return result

    def __invert__(self):
        """Transpose (~)."""
        result = dict()
        for key in self.keys():
            result[self[key]] = key
        return result

    def __contains__(self, other):
        """Contains key (in)."""
        return self.has_key(other)
    
    def __getattr__(self, key):
        """Get field or attribute (.)."""

        if key == '__methods__':
            return UserDict.__dict__.keys()

        if key == '__members__':
            return self.keys()
        
        if self.__dict__.has_key(key) or self.data.has_key(key):
            return self[key]

        raise AttributeError, key
                                
    def __str__(self):
        """Built-in pretty-printer."""
        return pformat(self.data)

# Ordered Dictionary Class
# ------------------------

class odict(dict):
    def __init__(self, *args, **kwds):
        self._keys = {}
        dict.__init__(self, *args, **kwds)

    def __delitem__(self, key):
        dict.__delitem__(self, key)
        del self._keys[key]

    def __setitem__(self, key, item):
        dict.__setitem__(self, key, item)
        if not self._keys.has_key(key):
            self._keys[key] = max([0] + self._keys.values()) + 1

    def clear(self):
        dict.clear(self)
        self._keys = {}

    def copy(self):
        result = odict(self)
        result._keys = self._keys.copy()
        return result

    def keys(self):
        result = [(y, x) for x, y in self._keys.items()]
        result.sort()
        return list([x[1] for x in result])

    def values(self):
        return list(map(self.get, self.keys()))

    def items(self):
        return list(zip(self.keys(), self.values()))

    def popitem(self):
        try:
            keys = [(y, x) for x, y in self._keys.items()]
            keys.sort()
            keys.reverse()
            key = keys[0][1]
            
        except IndexError:
            raise KeyError('dictionary is empty')

        val = self[key]
        del self[key]

        return (key, val)

    def setdefault(self, key, failobj=None):
        dict.setdefault(self, key, failobj)
        if not self._keys.has_key(key):
            self._keys[key] = max([0] + self._keys.values()) + 1

    def update(self, other):
        dict.update(self, other)
        for key in other.keys():
            if not self._keys.has_key(key):
                self._keys[key] = max([0] + self._keys.values()) + 1

# Custom Dictionary Constructors
# ------------------------------

# Dictionary set constructor. Elements must be hashable.
# Example: set('a', 'b', 'c') -> {'a': 1, 'b': 1, 'c': 1}
set = lambda *x, **y: dict(x, [1] * len(x), **y)

# Ordered dictionary set constructor. Elements must be hashable.
oset = lambda *x, **y: odict(x, [1] * len(x), **y)

# Dictionary histogram constructor. Elements must be hashable.
# Example: histo(['a', 'b', 'b', 'a', 'b', 'c']) -> {'a': 2, 'b': 3, 'c': 1}
histo  = lambda x, **y: list(x).reduce(_histo, dict(**y))
_histo = lambda x,   y: x.set(y, x.get(y, 0) + 1)

# Comparators
# -----------

# Case-insensitive, reversed, and reversed case-insensitive comparators.
cmpi    = lambda x, y: cmp(x.lower(), y.lower())
revcmp  = lambda x, y: cmp(y, x)
revcmpi = lambda x, y: cmp(y.lower(), x.lower())

def reorder(key, order):
    """
    Returns a comparator that reorders a row set (list of dictionaries).
    The order is specified as a key (column) and a list of ordered values.
    """
    return lambda x, y, k=key, o=dict(order, range(len(order))): \
                  cmp(o.get(x[k]), o.get(y[k]))

# Helper Functions
# ----------------

def curry(*args, **create_time_kwds):
    """
    Bind arguments to a function.
    
    Author: Alex Martelli
    Source: http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/52549
    """    
    func = args[0]
    create_time_args = args[1:]
    def curried_function(*call_time_args, **call_time_kwds):
        args = create_time_args + call_time_args
        kwds = create_time_kwds.copy()
        kwds.update(call_time_kwds)
        return func(*args, **kwds)
    return curried_function
