#!/usr/bin/env python
"""\
 Polynomial.py - A set of utilities to manipulate polynomials. This consists
 of a set of simple functions to convert polynomials to a Python list, and
 manipulate the resulting lists for multiplication, addition, and
 power functions. There is also a class that wraps these functions
 to make their use a little more natural.

 This can also evaluate the polynomials at a value, and take integrals
 and derivatives of the polynomials.

 Written by Rick Muller.
"""
import re

# Define some classes for some syntactic surgar:
class Polynomial:
    def __init__(self,val):
        if type(val) == type([]):
            self.plist = val
        elif type(val) == type(''):
            self.plist = parse_string(val)
        else:
            raise "Unknown argument to Polynomial: %s" % val
        return
    
    def __add__(self,other): return Polynomial(add(self.plist,plist(other)))
    def __radd__(self,other): return Polynomial(add(self.plist,plist(other)))
    def __sub__(self,other):  return Polynomial(sub(self.plist,plist(other)))
    def __rsub__(self,other): return -Polynomial(sub(self.plist,plist(other)))
    def __mul__(self,other): return Polynomial(multiply(self.plist,
                                                        plist(other)))
    def __rmul__(self,other): return Polynomial(multiply(self.plist,
                                                        plist(other)))
    def __neg__(self): return -1*self
    def __pow__(self,e): return Polynomial(power(self.plist,e))
    def __repr__(self): return tostring(self.plist)
    def __call__(self,x1,x2=None): return peval(self.plist,x1,x2)

    def integral(self): return Polynomial(integral(self.plist))
    def derivative(self): return Polynomial(derivative(self.plist))

# Define some simple utility functions. These manipulate "plists", polynomials
#  that are stored as python lists. Thus, 3x^2 + 2x + 1 would be stored
#  as [1,2,3] (lowest to highest power of x, even though polynomials
#  are typically written from highest to lowest power).

def plist(term):
    "Force term to have the form of a polynomial list"
    # First see if this is already a Polynomial object
    try:
        pl = term.plist
        return pl
    except:
        pass

    # It isn't. Try to force coercion from an integer or a float
    if type(term) == type(1.0) or type(term) == type(1):
        return [term]
    elif type(term) == type(''):
        return parse_string(term)
    # We ultimately want to be able to parse a string here
    else:
        raise "Unsupported term can't be corced into a plist: %s" % term
    return None

def peval(plist,x,x2=None):
    """\
    Eval the plist at value x. If two values are given, the
    difference between the second and the first is returned. This
    latter feature is included for the purpose of evaluating
    definite integrals.
    """
    val = 0
    if x2:
        for i in range(len(plist)): val += plist[i]*(pow(x2,i)-pow(x,i))
    else:
        for i in range(len(plist)): val += plist[i]*pow(x,i)
    return val

def integral(plist):
    """\
    Return a new plist corresponding to the integral of the input plist.
    This function uses zero as the constant term, which is okay when
    evaluating a definite integral, for example, but is otherwise
    ambiguous.

    The math forces the coefficients to be turned into floats.
    Consider importing __future__ division to simplify this.
    """
    if not plist: return []
    new = [0]
    for i in range(len(plist)):
        c = plist[i]/(i+1.)
        if c == int(c): c = int(c) # attempt to cast back to int
        new.append(c)
    return new

def derivative(plist):
    """\
    Return a new plist corresponding to the derivative of the input plist.
    """
    new = []
    if not plist: return new
    for i in range(1,len(plist)): new.append(i*plist[i])
    return new

def add(p1,p2):
    "Return a new plist corresponding to the sum of the two input plists."
    if len(p1) > len(p2):
        new = [i for i in p1]
        for i in range(len(p2)): new[i] += p2[i]
    else:
        new = [i for i in p2]
        for i in range(len(p1)): new[i] += p1[i]
    return new

def sub(p1,p2): return add(p1,mult_const(p2,-1))

def mult_const(p,c):
    "Return a new plist corresponding to the input plist multplied by a const"
    return [c*pi for pi in p]

def multiply(p1,p2):
    "Return a new plist corresponding to the product of the two input plists"
    if len(p1) > len(p2): short,long = p2,p1
    else: short,long = p1,p2
    new = []
    for i in range(len(short)): new = add(new,mult_one(long,short[i],i))
    return new

def mult_one(p,c,i):
    """\
    Return a new plist corresponding to the product of the input plist p
    with the single term c*x^i
    """
    new = [0]*i # increment the list with i zeros
    for pi in p: new.append(pi*c)
    return new

def power(p,e):
    "Return a new plist corresponding to the e-th power of the input plist p"
    assert int(e) == e, "Can only take integral power of a plist"
    new = [1]
    for i in range(e): new = multiply(new,p)
    return new

def parse_string(str=None):
    """\
    Do very, very primitive parsing of a string into a plist.
    'x' is the only term considered for the polynomial, and this
    routine can only handle terms of the form:
    7x^2 + 6x - 5
    and will choke on seemingly simple forms such as
    x^2*7 - 1
    or
    x**2 - 1
    """
    termpat = re.compile('([-+]?\s*\d*\.?\d*)(x?\^?\d?)')
    #print "Parsing string: ",str
    #print termpat.findall(str)
    res_dict = {}
    for n,p in termpat.findall(str):
        n,p = n.strip(),p.strip()
        if not n and not p: continue
        n,p = parse_n(n),parse_p(p)
        if res_dict.has_key(p): res_dict[p] += n
        else: res_dict[p] = n
    highest_order = max(res_dict.keys())
    res = [0]*(highest_order+1)
    for key,value in res_dict.items(): res[key] = value
    return res

def parse_n(str):
    "Parse the number part of a polynomial string term"
    if not str: return 1
    elif str == '-': return -1
    elif str == '+': return 1
    return eval(str)

def parse_p(str):
    "Parse the power part of a polynomial string term"
    pat = re.compile('x\^?(\d)?')
    if not str: return 0
    res = pat.findall(str)[0]
    if not res: return 1
    return int(res)

def strip_leading_zeros(p):
    "Remove the leading (in terms of high orders of x) zeros in the polynomial"
    # compute the highest nonzero element of the list
    for i in range(len(p)-1,-1,-1):
        if p[i]: break
    return p[:i+1]

def tostring(p):
    """\
    Convert a plist into a string. This looks overly complex at first,
    but most of the complexity is caused by special cases.
    """
    p = strip_leading_zeros(p)
    str = []
    for i in range(len(p)-1,-1,-1):
        if p[i]:
            if i < len(p)-1:
                if p[i] >= 0: str.append('+')
                else: str.append('-')
                str.append(tostring_term(abs(p[i]),i))
            else:
                str.append(tostring_term(p[i],i))
    return ' '.join(str)

def tostring_term(c,i):
    "Convert a single coefficient c and power e to a string cx^i"
    if i == 1:
        if c == 1: return 'x'
        elif c == -1: return '-x'
        return "%sx" % c
    elif i: 
        if c == 1: return "x^%d" % i
        elif c == -1: return "-x^%d" % i
        return "%sx^%d" % (c,i)
    return "%s" % c

def test():
    print tostring([1,2.,3]) # testing floats
    print tostring([1,2,-3]) # can we handle - signs
    print tostring([1,-2,3])
    print tostring([0,1,2])  # are we smart enough to exclude 0 terms?
    print tostring([0,1,2,0]) # testing leading zero stripping
    print tostring([0,1])
    print tostring([0,1.0]) # testing whether 1.0 == 1: risky
    print tostring(add([1,2,3],[1,-2,3]))  # test addition
    print tostring(multiply([1,1],[-1,1])) # test multiplication
    print tostring(power([1,1],2))         # test power

    # Some cases using the polynomial objects:
    print Polynomial([1,2,3]) + Polynomial([1,2]) # add
    print Polynomial([1,2,3]) + 1                 # add
    print Polynomial([1,2,3])-1                   # sub
    print 1-Polynomial([1,2,3])                   # rsub
    print 1+Polynomial([1,2,3])                   # radd
    print Polynomial([1,2,3])*-1                  # mul
    print -1*Polynomial([1,2,3])                  # rmul
    print -Polynomial([1,2,3])                    # neg
    print ''
    # Work out Niklasson's raising and lowering operators:
    #  tests putting constants into the polynomial.
    for m in range(1,4):
        print 'P^a_%d = ' % m,\
              1 - Polynomial([1,-1])**m*Polynomial([1,m])
        print 'P^b_%d = ' % m,\
              Polynomial([0,1])**m*Polynomial([1+m,-m])
    print ''

    # Test string parsing
    print parse_string('+3x - 4x^2 + 7x^5-x+1')
    print Polynomial(parse_string('+3x - 4x^2 + 7x^5-x+1'))
    print Polynomial('+3x - 4x^2 + 7x^5-x+1')
    print Polynomial('+3x -4x^2+7x^5-x+1') - 7
    print Polynomial('5x+x^2')

    # Test the integral and derivatives
    print integral([])
    print integral([1])
    print integral([0,1])
    print derivative([0,0,0.5])
    p = Polynomial('x')
    ip = p.integral()
    dp = p.derivative()
    print ip,dp
    print ip(0,1) # integral of y=x from (0,1)

if __name__ == '__main__': test()
