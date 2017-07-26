#!/usr/bin/env python
# 
# a python vector class
# A. Pletzer 5 Jan 00/11 April 2002
#
import math

"""
A list based vector class that supports elementwise mathematical operations

In this version, the vector call inherits from list; this 
requires Python 2.2 or later.
"""

class vector(list):
	"""
        A list based vector class
	"""
	# no c'tor

	def __getslice__(self, i, j):
		try:
			# use the list __getslice__ method and convert
			# result to vector
			return vector(super(vector, self).__getslice__(i,j))
		except:
			raise TypeError, 'vector::FAILURE in __getslice__'
		
	def __add__(self, other):
		return vector(map(lambda x,y: x+y, self, other))

	def __neg__(self):
		return vector(map(lambda x: -x, self))
	
	def __sub__(self, other):
		return vector(map(lambda x,y: x-y, self, other))

	def __mul__(self, other):
	    """
	    Element by element multiplication
	    """
	    try:
		    return vector(map(lambda x,y: x*y, self,other))
	    except:
		    # other is a const
		    return vector(map(lambda x: x*other, self))


	def __rmul__(self, other):
		return (self*other)


	def __div__(self, other):
	    """
	    Element by element division.
	    """
	    try:
		    return vector(map(lambda x,y: x/y, self, other))
	    except:
		    return vector(map(lambda x: x/other, self))

	def __rdiv__(self, other):
	    """
	    The same as __div__
	    """
	    try:
		    return vector(map(lambda x,y: x/y, other, self))
	    except:
		    # other is a const
		    return vector(map(lambda x: other/x, self))

        def size(self): return len(self)

	def conjugate(self):
	    return vector(map(lambda x: x.conjugate(), self))

        def ReIm(self):
		"""
		Return the real and imaginary parts
		"""
		return [
			vector(map(lambda x: x.real, self)),
			vector(map(lambda x: x.imag, self)),
			]
	
        def AbsArg(self):
		"""
		Return modulus and phase parts
		"""
		return [
			vector(map(lambda x: abs(x), self)),
			vector(map(lambda x: math.atan2(x.imag,x.real), self)),
			]


	def out(self):
	    """
	    Prints out the vector.
	    """
	    print self

###############################################################################


def isVector(x):
    """
    Determines if the argument is a vector class object.
    """
    return hasattr(x,'__class__') and x.__class__ is vector

def zeros(n):
    """
    Returns a zero vector of length n.
    """
    return vector(map(lambda x: 0., range(n)))

def ones(n):
    """
    Returns a vector of length n with all ones.
    """
    return vector(map(lambda x: 1., range(n)))

def random(n, lmin=0.0, lmax=1.0):
    """
    Returns a random vector of length n.
    """
    import whrandom
    new = vector([])
    gen = whrandom.whrandom()
    dl = lmax-lmin
    return vector(map(lambda x: dl*gen.random(),
		       range(n)))
	
def dot(a, b):
    """
    dot product of two vectors.
    """
    try:
	return reduce(lambda x, y: x+y, a*b, 0.)
    except:
	raise TypeError, 'vector::FAILURE in dot'
	

def norm(a):
    """
    Computes the norm of vector a.
    """
    try:
	return math.sqrt(abs(dot(a,a)))
    except:
	raise TypeError, 'vector::FAILURE in norm'

def sum(a):
    """
    Returns the sum of the elements of a.
    """
    try:
	return reduce(lambda x, y: x+y, a, 0)
    except:
	raise TypeError, 'vector::FAILURE in sum'

# elementwise operations
	
def log10(a):
    """
    log10 of each element of a.
    """
    try:
	return vector(map(math.log10, a))
    except:
	raise TypeError, 'vector::FAILURE in log10'

def log(a):
    """
    log of each element of a.
    """
    try:
	return vector(map(math.log, a))
    except:
	raise TypeError, 'vector::FAILURE in log'
	    
def exp(a):
    """
    Elementwise exponential.
    """
    try:
	return vector(map(math.exp, a))
    except:
	raise TypeError, 'vector::FAILURE in exp'

def sin(a):
    """
    Elementwise sine.
    """
    try:
	return vector(map(math.sin, a))
    except:
	raise TypeError, 'vector::FAILURE in sin'
	    
def tan(a):
    """
    Elementwise tangent.
    """
    try:
	return vector(map(math.tan, a))
    except:
	raise TypeError, 'vector::FAILURE in tan'
	    
def cos(a):
    """
    Elementwise cosine.
    """
    try:
	return vector(map(math.cos, a))
    except:
	raise TypeError, 'vector::FAILURE in cos'

def asin(a):
    """
    Elementwise inverse sine.
    """
    try:
	return vector(map(math.asin, a))
    except:
	raise TypeError, 'vector::FAILURE in asin'

def atan(a):
    """
    Elementwise inverse tangent.
    """	
    try:
	return vector(map(math.atan, a))
    except:
	raise TypeError, 'vector::FAILURE in atan'

def acos(a):
    """
    Elementwise inverse cosine.
    """
    try:
	return vector(map(math.acos, a))
    except:
	raise TypeError, 'vector::FAILURE in acos'

def sqrt(a):
    """
    Elementwise sqrt.
    """
    try:
	return vector(map(math.sqrt, a))
    except:
	raise TypeError, 'vector::FAILURE in sqrt'

def sinh(a):
    """
    Elementwise hyperbolic sine.
    """
    try:
	return vector(map(math.sinh, a))
    except:
	raise TypeError, 'vector::FAILURE in sinh'

def tanh(a):
    """
    Elementwise hyperbolic tangent.
    """
    try:
	return vector(map(math.tanh, a))
    except:
	raise TypeError, 'vector::FAILURE in tanh'

def cosh(a):
    """
    Elementwise hyperbolic cosine.
    """
    try:
	return vector(map(math.cosh, a))
    except:
	raise TypeError, 'vector::FAILURE in cosh'


def pow(a,b):
    """
    Takes the elements of a and raises them to the b-th power
    """
    try:
        return vector(map(lambda x: x**b, a))
    except:
        try:
		return vector(map(lambda x,y: x**y, a, b))
	except:
		raise TypeError, 'vector::FAILURE in pow'
	
def atan2(a,b):    
    """
    Arc tangent
    
    """
    try:
	return vector(map(math.atan2, a, b))
    except:
	raise TypeError, 'vector::FAILURE in atan2'
	

###############################################################################
if __name__ == "__main__":

	print 'a = zeros(4)'
	a = zeros(4)

	print 'a.__doc__=',a.__doc__

	print 'a[0] = 1.0'
	a[0] = 1.0

	print 'a[3] = 3.0'
	a[3] = 3.0

	print 'a[0]=', a[0]
	print 'a[1]=', a[1]

	print 'len(a)=',len(a)
	print 'a.size()=', a.size()
			
	b = vector([1, 2, 3, 4])
	print 'a=', a
	print 'b=', b

	print 'a+b'
	c = a + b
	c.out()

	print '-a'
	c = -a
	c.out()
	a.out()

	print 'a-b'
	c = a - b
	c.out()

	print 'a*1.2'
	c = a*1.2
	c.out()


	print '1.2*a'
	c = 1.2*a
	c.out()
	print 'a=', a

	print 'dot(a,b) = ', dot(a,b)
	print 'dot(b,a) = ', dot(b,a)

	print 'a*b'
	c = a*b
	c.out()
	
	print 'a/1.2'
	c = a/1.2
	c.out()

	print 'a[0:2]'
	c = a[0:2]
	c.out()

	print 'a[2:5] = [9.0, 4.0, 5.0]'
	a[2:5] = [9.0, 4.0, 5.0]
	a.out()

	print 'sqrt(a)=',sqrt(a)
	print 'pow(a, 2*ones(len(a)))=',pow(a, 2*ones(len(a)))
	print 'pow(a, 2)=',pow(a, 2*ones(len(a)))

	print 'ones(10)'
	c = ones(10)
	c.out()

	print 'zeros(10)'
	c = zeros(10)
	c.out()	

	print 'del a'
	del a

	try:
		a = random(11, 0., 2.)
		a.out()

	except: pass
