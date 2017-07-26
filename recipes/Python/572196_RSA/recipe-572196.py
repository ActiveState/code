#!/usr/bin/python
# -*- coding: utf-8 -*-
"""\
The author takes no responsibility for anything having anything to do
with this code. Use at your own risk, or don't use at all.

This is a Python implementation functions used in the RSA algorithm, as
well as a file-like object for writing encrypted files that it can later
read using the same password. This is useful for if you want store
sensitive data to a file with a user-given password.

The RSA keys are obtained as follows:
1. Choose two prime numbers p and q
2. Compute n=pq
3. Compute φ(n)=totient(p,q)
4. Choose e coprime to φ(n) such that gcd(e,n)=1
5. Compute d=modInverse(e,φ(n))
6. e is the publickey; n is also made public; d is the privatekey

Encryption is as follows:
1. Size of data to be encrypted must be less than n
2. ciphertext=pow(plaintext,publickey,n)

Decryption is as follows:
1. Size of data to be encrypted must be less than n
2. plaintext=pow(ciphertext,privatekey,n)
"""

import random,md5

def RabinMillerWitness(test,possible):
	#calculates (a**b)%n via binary exponentiation, yielding itermediate
	#results as Rabin-Miller requires
	#written by Josiah Carlson
	#modified and optimized by Collin Stocks
	a,b,n=long(test%possible),possible-1,possible
	if a==1:
		return False
	A=a
	t=1L
	while t<=b:
		t<<=1
	#t=2**k, and t>b
	t>>=2
	while t:
		A=pow(A,2,n)
		if t&b:
			A=(A*a)%n
		if A==1:
			return False
		t>>=1
	return True

smallprimes = (3,5,7,11,13,17,19,23,29,31,37,41,43,
				47,53,59,61,67,71,73,79,83,89,97)

def getPrime(b,seed):
	#Generates an integer of b bits that is probably prime
	#written by Josiah Carlson
	#modified (heavily) and optimized by Collin Stocks
	bits=int(b)
	assert 64<=bits
	k=bits<<1
	possible=seed|1 # make it odd
	good=0
	while not good:
		possible+=2 # keep it odd
		good=1
		for i in smallprimes:
			if possible%i==0:
				good=0
				break
		else:
			for i in xrange(k):
				test=random.randrange(2,possible)|1
				if RabinMillerWitness(test,possible):
					good=0
					break
	return possible

def egcd(a,b):
	# Extended Euclidean Algorithm
	# returns x, y, gcd(a,b) such that ax + by = gcd(a,b)
	u, u1 = 1, 0
	v, v1 = 0, 1
	while b:
		q = a // b
		u, u1 = u1, u - q * u1
		v, v1 = v1, v - q * v1
		a, b = b, a - q * b
	return u, v, a

def gcd(a,b):
	# 2.8 times faster than egcd(a,b)[2]
	a,b=(b,a) if a<b else (a,b)
	while b:
		a,b=b,a%b
	return a

def modInverse(e,n):
	# d such that de = 1 (mod n)
	# e must be coprime to n
	# this is assumed to be true
	return egcd(e,n)[0]%n

def totient(p,q):
	# Calculates the totient of pq
	return (p-1)*(q-1)

def passwordToPrimePair(pswd,bits=64):
	assert 64<=bits
	assert bits%4==0
	length=bits//4
	sep=len(pswd)//2
	append="0"*(length-sep)
	seed1=int(pswd[:sep]+append,16)
	seed2=int(pswd[sep:]+append,16)
	p=getPrime(bits,seed1)
	q=getPrime(bits,seed2)
	return p,q

def passwordToKey(password,bits=64):
	assert 64<=bits
	assert bits%4==0
	length=bits//4
	pswd=md5.new(password).hexdigest()
	p,q=passwordToPrimePair(pswd,bits)
	n=p*q
	append="0"*(length-len(pswd))
	possible=int(pswd+append,16)|1 # n is always even
							# so possible must be odd
	while not gcd(possible,n):
		possible+=2 # keep it odd
	private=possible
	public=modInverse(private,totient(p,q))
	return public,private,n

def crypt(string,power,n):
	data1=0L
	for char in string:
		data1<<=8
		data1+=ord(char)
	data2=pow(data1,power,n)
	ret=""
	while data2:
		data2,r=divmod(data2,256)
		ret=chr(r)+ret
	return ret

def encrypt(string,power,n,bits=128):
	string=string.replace('/',"/s").replace('\0',"/0") # escape \x00
				# because crypt() ignores leading zeros
	bytes=bits//8
	lst=[]
	while string:
		lst.append(string[:bytes-1]) # string must have a lesser value than
		string=string[bytes-1:] # n, so truncate and pad
	for i in range(len(lst)):
		lst[i]=crypt(lst[i],power,n)
		lst[i]='\0'*(bytes-len(lst[i]))+lst[i] # pad with zeros
			# don't worry about removing these later: crypt() ignores
			# leading zeros already, so they are always removed
	return ''.join(lst) # the length of this must be a multiple of bytes

def decrypt(string,power,n,bits=128):
	bytes=bits//8
	lst=[]
	while string:
		lst.append(string[:bytes])
		string=string[bytes:]
	for i in range(len(lst)):
		lst[i]=crypt(lst[i],power,n)
	ret=''.join(lst)
	ret=ret.replace("/0",'\0').replace("/s",'/')
	return ret

#			data=data.replace('/',"/s").replace('\0',"/0")
#			data=data.replace("/0",'\0').replace("/s",'/')

class secureFile(object):
	# Provides a file-like object for creating secure files that it can
	# later read. It takes a string as a password that it uses to generate
	# both prime numbers and the encryption key.
	def __init__(self,fileobj,password,bits=128,mode="rb"):
		# Function must be passed an open file or a file name,
		# and on operating systems where this matters, the
		# binary attribute must be set.
		# For example, open("file","rb"), not open("file","r")
		if type(fileobj)==str:
			fileobj=open(fileobj,mode)
		self.f=fileobj
		self.e,self.d,self.n=passwordToKey(password,bits//2)
		self.bits=bits
		self.rbuf=""
		self.wbuf=""
	def write(self,data):
		self.wbuf+=data
		e,n,bits,bytes=self.e,self.n,self.bits,self.bits//8
		while bytes<len(self.wbuf):
			self.f.write(encrypt(self.data[:bytes],e,n,bits))
			self.wbuf=self.wbuf[bytes:]
	def flush(self):
		self.f.write(encrypt(self.wbuf,self.e,self.n,self.bits))
		self.wbuf=""
	def read(self,bytes=None):
		if bytes==None:
			self.rbuf+=decrypt(self.f.read(),self.d,self.n,self.bits)
			ret=self.rbuf
			self.rbuf=""
		else:
			_bytes=bytes-len(self.rbuf)
			rbytes=_bytes+(self.bits-_bytes%self.bits)
			self.rbuf+=decrypt(self.f.read(rbytes),self.d,self.n,self.bits)
			ret=self.rbuf[:bytes]
			self.rbuf=self.rbuf[bytes:]
		return ret
	def readline(self):
		ret=""
		while not ret.endswith('\n'):
			ln=len(ret)
			ret+=self.read(1)
			if len(ret)==ln:
				break
		return ret
	def readlines(self):
		ret=[]
		while ret[-1]:
			ret.append(self.readline())
		return ret[:-1]
	def next(self):
		ret=self.readline()
		if len(ret)==0:
			raise StopIteration
	def __iter__(self):
		return self
	def close(self):
		self.flush()
		self.f.close()

try:
	import psyco
	psyco.bind(RabinMillerWitness)
	psyco.bind(getPrime)
	psyco.bind(egcd)
	psyco.bind(gcd)
	psyco.bind(modInverse)
	psyco.bind(totient)
	psyco.bind(passwordToPrimePair)
	psyco.bind(passwordToKey)
	psyco.bind(crypt)
	psyco.bind(encrypt)
	psyco.bind(decrypt)
	psyco.bind(secureFile)
except ImportError:
	pass

if __name__=="__main__":
	print passwordToKey(raw_input("Password: "))
