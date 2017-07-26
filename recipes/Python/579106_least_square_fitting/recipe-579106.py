#!/usr/bin/env python3

"""
reference:
http://www.geometrictools.com/Documentation/LeastSquaresFitting.pdf
"""

import numpy as np
import numpy.matlib as mat
	
class _CurveFit() :
	def __init__(self, * coef) :
		if len(coef) == 1 :
			coef = list(coef)
		if  len(coef) == len(self.coef) :
			self.coef = np.array(coef, dtype=np.float64)
		elif len(coef) != 0 :
			raise ValueError("Curve is defined by {0} parameters".format(len(self.coef)))

	def image(self, * v) :
		return (self._order(* v) * self.coef).sum()

	def fit(self, * p_list) :
		A = mat.zeros((6, 6))
		Y = mat.zeros((6, 1))
		for x, y, z in p_list :
			Q = np.asmatrix(self._order(x, y)).T
			A += Q * Q.T
			Y += z * Q
		self.coef = np.array(np.ravel(A.I * Y))
		return self

class Paraboloid(_CurveFit) :
	# coef must be defined by default, length must be the same as the return value of self._order()
	coef = np.array([1.0, 1.0, 1.0, 1.0, 1.0, 1.0], dtype=np.float64)
	
	def _order(self, x, y) :
		return np.array([x**2, x*y, y**2, x, y, 1])

if __name__ == '__main__' :
	p = Paraboloid(1, 2, 3, 4, 5, -1)
	z = list()
	for x in range(-2, 3) :
		for y in range(-2, 3) :
			z.append((x, y, p.image(x, y)))
	q = Paraboloid().fit(* z)
	print("original   =", p.coef)
	print("estimation =", q.coef)	
	assert(np.allclose(q.coef, p.coef))
	
	
