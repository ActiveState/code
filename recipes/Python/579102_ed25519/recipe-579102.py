#!/usr/bin/env python3

"""
this code is a cleaned version of http://ed25519.cr.yp.to/python/ed25519.py for python3

code released under the terms of the GNU Public License v3, copyleft 2015 yoochan
"""

import collections
import hashlib
import os
import random

Point = collections.namedtuple('Point', ['x', 'y'])

key_mask = int.from_bytes(b'\x3F' + b'\xFF' * 30 + b'\xF8', 'big', signed=False)

class Ed25519() :
	
	length = 256

	def __init__(self) :
		self.q = 2**255 - 19
		self.l = 2**252 + 27742317777372353535851937790883648493
		self.d = -121665 * self.inverse(121666)
		
		self.i = pow(2, (self.q - 1)//4, self.q)
		
		self.B = self.point(4 * self.inverse(5))
		
	def to_hash(self, m) :
		return hashlib.sha512(m).digest()
		
	def from_bytes(self, h) :
		""" pick 32 bytes, return a 256 bit int """
		return int.from_bytes(h[0:self.length//8], 'little', signed=False)
		
	def to_bytes(self, k) :
		return k.to_bytes(self.length//8, 'little', signed=False)
		
	def as_key(self, h) :
		return 2**(self.length-2) + (self.from_bytes(h) & key_mask)
		
	def secret_key(self) :
		""" pick a random secret key """
		m = os.urandom(1024)
		h = self.to_hash(m)
		k = self.as_key(h)
		return self.to_bytes(k)
		
	def public_key(self, sk) :
		""" compute the public key from the secret one """
		h = self.to_hash(sk)
		a = self.as_key(h)
		c = self.outer(self.B, a)
		return self.point_to_bytes(c)
		
	def inverse(self, x) :
		return pow(x, self.q - 2, self.q)
		
	def sign(self, message, secret_key, public_key) :
		s_h = self.to_hash(secret_key)
		s_d = self.as_key(s_h)
		
		m_h = self.to_hash(s_h[self.length//8:self.length//4] + message)
		m_d = self.from_bytes(m_h)
		
		R = self.outer(self.B, m_d)
		
		r_h = self.to_hash(self.point_to_bytes(R) + public_key + message)
		r_d = m_d + self.from_bytes(r_h) * s_d
		
		return self.point_to_bytes(R) + self.to_bytes(r_d % self.l)
		
	def verify(self, message, signature, public_key) :
		r_b = signature[0:self.length//8]
		r_h = self.to_hash(r_b + public_key + message)
		r_d = self.from_bytes(r_h)
		
		s_d = self.from_bytes(signature[self.length//8:self.length//4])
		b_j = self.outer(self.B, s_d)
		
		P = self.bytes_to_point(public_key)
		p_j = self.outer(P, r_d)
		
		R = self.bytes_to_point(r_b)
		
		return b_j == self.inner(R, p_j)
		
	def recover(self, y) :
		""" given a value y, recover the preimage x """
		p = (y*y - 1) * self.inverse(self.d*y*y + 1)
		x = pow(p, (self.q + 3)//8, self.q)
		if (x*x - p) % self.q != 0:
			x = (x * self.i) % self.q
		if x % 2 != 0 :
			x = self.q - x
		return x
		
	def point(self, y) :
		""" given a value y, recover x and return the corresponding P(x, y) """
		return Point(self.recover(y) % self.q, y % self.q)
	
	def is_on_curve(self, P) :
		return (P.y*P.y - P.x*P.x - 1 - self.d*P.x*P.x*P.y*P.y) % self.q == 0
		
	def inner(self, P, Q) :
		""" inner product on the curve, between two points """
		x = (P.x*Q.y + Q.x*P.y) * self.inverse(1 + self.d*P.x*Q.x*P.y*Q.y)
		y = (P.y*Q.y + P.x*Q.x) * self.inverse(1 - self.d*P.x*Q.x*P.y*Q.y)
		return Point(x % self.q, y % self.q)
		
	def outer(self, P, n) :
		""" outer product on the curve, between a point and a scalar """
		if n == 0:
			return Point(0, 1)
		Q = self.outer(P, n//2)
		Q = self.inner(Q, Q)
		if n & 1:
			Q = self.inner(Q, P)
		return Q
		
	def point_to_bytes(self, P) :
		return (P.y + ((P.x & 1) << 255)).to_bytes(self.length//8, 'little')
		
	def bytes_to_point(self, b) :
		i = self.from_bytes(b)
		y = i % 2**(self.length - 1)
		x = self.recover(y)
		if (x & 1) != ((i >> (self.length-1)) & 1) :
			x = self.q - x
		return Point(x, y)

if __name__ == '__main__' :
	def hexit(s) :
		return ''.join("{0:02X}".format(i) for i in reversed(s))
		
	ecc = Ed25519()
	
	alice_sk = b'alicealicealicealicealicealiceal' # ecc.secret_key()
	alice_pk = ecc.public_key(alice_sk)
	
	assert(hexit(alice_pk) == 'AFA095BF733298216D0E88A0F2A4FEB15E5FEB73E7FA7522B67594FD2EF770D6')
	
	message = 'foo bar'.encode('utf8')
	signature = ecc.sign(message, alice_sk, alice_pk)
	
	import cProfile
	cProfile.run("ecc.sign(message, alice_sk, alice_pk)")
	
	assert(ecc.verify(message, signature, alice_pk))
	cProfile.run("ecc.verify(message, signature, alice_pk)")
	
	print("code test: OK")
	
