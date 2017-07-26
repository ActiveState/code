def primepow(aNumber):
	'''finds the prime base P and power N such that aNumber = P^N.'''
	firstfactor = 0
	p = 0
	n = 0
	if aNumber <= 1: 
		return False
	if isprime(aNumber):
		p = aNumber
		n = 1
		return (p, n)
	else: 
	  	for k in xrange(2, int(math.sqrt(aNumber+1))+1):
	  		if ( ( aNumber % k ) == 0 ):
	  			firstfactor = k
	  			break
	  			
	  	if ( False == isprime( firstfactor ) ):
	  		return False
  		  
  		q = aNumber
  		while( True ):
  			if q == 1:
  				return (firstfactor, n)
  			if (q % firstfactor) == 0:
  				n = n + 1
  				q = q / firstfactor
  			else:
  				return False
