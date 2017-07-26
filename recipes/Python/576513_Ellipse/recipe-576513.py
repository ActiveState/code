#On the name of ALLAH
#Author : Fouad Teniou
#Date : 23/09/08
#Version 2.4

import math as m

Class Ellipse:
	""" Class that represent an ellipse """
	def __call__(self,**kargs):	# ** allows to convert from keywords to dictionary
		""" Python run  __call__ method for function call expressions applied to instance """
		self.kargs = kargs
		self._a = "%2.1f"
		self._b = chr(253)
		self._c = self._a% m.sqrt(self.kargs.get('a'))
		self._d = self._a% m.sqrt(self.kargs.get('b'))
		self._e = self._a% m.sqrt(abs(self.kargs.get('a') - self.kargs.get('b'))
		self._f = self._a% m.sqrt(abs(self.kargs.get('b') - self.kargs.get('a'))

		#Determine if Ellipse equation should be displayed, based on keys’ values
		if (len(kargs) == 2 and self.kargs.has_key('a') and self.kargs.get('a') != 0
			and self.kargs.has_key('b') and self.kargs.get('b') !=0
			and self.kargs.get('a') != self.kargs.get('b')):
			if self.kargs.get('a') > self.kargs.get('b'):
				self._e
			else:
				self._f
		#raise ValueError if one or more of keys’ values are not appropriate 
		else:
			raise ValueError, \
				("\n<Ellipse equation should be of the form : \
				   \nx%s/a%s + y%s/b%s = 1 or x%s/b%s + y%s/a%s = 1 (a!=0 and b!=0) " % \
				  (self._b,self._b,self._b,self._b,self._b,self._b,self._b,self._b)
	def __str__(self):
		""" String representation of an ellipse """
		if self.kargs.get('a') > self.kargs.get('b')
			return "\n<Ellipse function x%s\%s + y%s\%s = 1: x%s has the larger dominator , the major axis is along the x -axis \
			\n\n-- The coordinates of the foci are : (%s,0) and (-%s,0) \
			\n\n-- Drawing a box extending a = %s on each side of the origin along the x-axis and extending \
			\n   b = %s on each side of the origin along the y-axis as a guide yield the graph" % \
			           (self._b,self.kargs.get('a'),self._b,self.kargs.get('b'),self._b,self._e,self._e,self._c,self._d)
		else:
			return "\n<Ellipse function x%s\%s + y%s\%s = 1: y%s has the larger dominator , the major axis is along the y- axis \
			\n\n-- The coordinates of the foci are : (0, %s) and (0,-%s) \
			\n\n-- Drawing a box extending a = %s on each side of the origin along the y-axis and extending \
			\n   b = %s on each side of the origin along the x-axis as a guide yield the graph" % \
			           (self._b,self.kargs.get('a'),self._b,self.kargs.get('b'),self._b,self._f,self._f,self._d,self._c)
if __name__ == "__main__":
	test = Ellipse()
	test(a=4,b=2)
	print test
	test(a=17,b=25)
	print test
	test(a=0, b= 5)
	print test

				
