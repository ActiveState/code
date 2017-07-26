class PrimeList:
	def __init__(self, initial=0):
		self.primelist = [2]
		self.primelookup = [0,0,1,1]
		self.max_prime = 2
		self.initialise_list(initial)

	def initialise_list(self,upto):
		"Good old Sieve of Eratosthenes"
		if upto <= 3:
			pass
		self.primelookup.extend([0,1] * ((upto-3)//2))
		if upto % 2 == 0:
			self.primelookup.extend([0])
		for i in range(3, upto + 1 , 2):
			if self.primelookup[i]:
				self.primelist.append(i)
				self.max_prime = i
				j = i + i
				while j <= upto:
					self.primelookup[j] = 0
					j += i

	def __contains__(self,number):
		if number < 2:
			return False
		if number > self.max_prime - 1:
			#print "Asking for what I dont have!"
			return self._isprime(number)
		return self.primelookup[number]

	def _isprime(self, number):
		for prime in self.primelist:
			if prime > number ** .5:
				break
			if number % prime == 0:
				return False
		if number < self.max_prime ** 2:
			return True
		else:
			#Brute forcing
			for i in range(self.max_prime,number ** .5 + 1, 2):
				if number % i == 0:
					return False
			return True
