#!/usr/bin/env python

def prime(n):
	"""
	Generate all prime numbers less than n.
	"""
	yield 2
	primes = []
	for m in range(3,n,2):
		if all(m%p for p in primes):
			primes.append(m)
			yield m

def main():
	print list(prime(1000))

	#or a slower one-liner
	print [n for n in range(3,1000,2) if all(n%p for p in range(3,n,2))]

if __name__=="__main__":
	main()
