#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import math
import random 
#y^2=x^3+ax+b mod n 

prime=[2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271 ]


# ax+by=gcd(a,b). This function returns [gcd(a,b),x,y]. Source Wikipedia
def extended_gcd(a,b):   
	x,y,lastx,lasty=0,1,1,0
	while b!=0:
		q=a/b
		a,b=b,a%b
		x,lastx=(lastx-q*x,x)
		y,lasty=(lasty-q*y,y)
	if a<0: 
		return (-a,-lastx,-lasty)
	else:
		return (a,lastx,lasty)

# pick first a point P=(u,v) with random non-zero coordinates u,v (mod N), then pick a random non-zero A (mod N), 
# then take B = u^2 - v^3 - Ax (mod N).
# http://en.wikipedia.org/wiki/Lenstra_elliptic_curve_factorization

def randomCurve(N):
	A,u,v=random.randrange(N),random.randrange(N),random.randrange(N)
        B=(v*v-u*u*u-A*u)%N
        return [(A,B,N),(u,v)]

	# Given the curve y^2 = x^3 + ax + b over the field K (whose characteristic we assume to be neither 2 nor 3), and points
	# P = (xP, yP) and Q = (xQ, yQ) on the curve, assume first that xP != xQ. Let the slope of the line s = (yP − yQ)/(xP − xQ); since K 	       # is a field, s is well-defined. Then we can define R = P + Q = (xR, − yR) by
	#	s=(xP-xQ)/(yP-yQ) Mod N		
	#	xR=s^2-xP-xQ	Mod N
	#	yR=yP+s(xR-xP)	Mod N 
	# If xP = xQ, then there are two options: if yP = −yQ, including the case where yP = yQ = 0, then the sum is defined as 0[Identity]. 	       # thus, the inverse of each point on the curve is found by reflecting it across the x-axis. If yP = yQ != 0, then R = P + P = 2P = 	      # (xR, −yR) is given by
	#	s=3xP^2+a/(2yP)	Mod N	
	#	xR=s^2-2xP	Mod N
	#	yR=yP+s(xR-xP)	Mod N
	#	http://en.wikipedia.org/wiki/Elliptic_curve#The_group_law''')
	
def addPoint(E,p_1,p_2):
	if p_1=="Identity": return [p_2,1]
	if p_2=="Identity": return [p_1,1]
	a,b,n=E
	(x_1,y_1)=p_1
	(x_2,y_2)=p_2
	x_1%=n
	y_1%=n
	x_2%=n
	y_2%=n
	if x_1 != x_2 :
		d,u,v=extended_gcd(x_1-x_2,n)
		s=((y_1-y_2)*u)%n
		x_3=(s*s-x_1-x_2)%n
		y_3=(-y_1-s*(x_3-x_1))%n
	else:
		if (y_1+y_2)%n==0:return ["Identity",1]
		else:
			d,u,v=extended_gcd(2*y_1,n)
			s=((3*x_1*x_1+a)*u)%n
			x_3=(s*s-2*x_1)%n
			y_3=(-y_1-s*(x_3-x_1))%n

	return [(x_3,y_3),d]

	# http://en.wikipedia.org/wiki/Elliptic_curve_point_multiplication
	#	Q=0 [Identity element]
	#	while m:
	#		if (m is odd) Q+=P
	#		P+=P
	#		m/=2
	#	return Q')

def mulPoint(E,P,m):
	Ret="Identity"
	d=1
	while m!=0:
		if m%2!=0: Ret,d=addPoint(E,Ret,P)
		if d!=1 : return [Ret,d]  # as soon as i got anything otherthan 1 return 
		P,d=addPoint(E,P,P)
		if d!=1 : return [Ret,d]
		m>>=1
	return [Ret,d]




def ellipticFactor(N,m,times=5):
	for i in xrange(times):
		E,P=randomCurve(N);
		Q,d=mulPoint(E,P,m)
		if d!=1 : return d
	return N

if __name__=="__main__":
	n=input()
	for p in prime:#preprocessing
		while n%p==0:
			print p
			n/=p
	m=int(math.factorial(2000))
	while n!=1:
		k=ellipticFactor(n,m)
		n/=k
		print k
