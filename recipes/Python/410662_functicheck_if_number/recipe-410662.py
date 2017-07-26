def isprime(aNumber):
	'''return True if the number is prime, false otherwise'''
	if aNumber < 2: return False
	if aNumber == 2: return True
	if (( aNumber / 2 ) * 2 == aNumber) : 
		return False
	else:
		klist = primes(int(math.sqrt(aNumber+1)))
		for k in klist[1:]:
			if (( aNumber / k ) * k == aNumber ): return False
		return True
