###############################################################################
# Evolution optimization strategy, based on genes frequency in genotype.      #
# Suitable for solving NP-complete problems such as generating sudoku game,   #
# tasks scheduling, designing networks and etc.                               #
# Algorithm idea is taken from:                                               #
# http://www.cad.polito.it/FullDB/exact/sac98.html                            #
# Implemented by: vasiliauskas.agnius@gmail.com                               #
###############################################################################

import random

class sgaLocus:
	"""
	Class for defining allele position (locus) in genome
	"""
	def __init__(self, Alleles):
		self.Genes = [None, None, None]  # [FirstGenome, SecondGenome, BestGenome]
		self.Alleles = dict([(x, 1.0/len(Alleles)) for x in Alleles])

class sgaGenotype:
	"""
	Class for defining population genotype.
	Main class for evolving problem solutions
	"""
	def __init__(self, alleleGroups, Amount, FitnessFunc, NotifyFunc = None, Minimize = True):
		self.FitnessFunc = FitnessFunc
		self.NotifyFunc = NotifyFunc
		self.Minimize = Minimize
		self.AlleleAffectValue = 0.005
		self.Fitness = [None, None, None]  # [FirstGenome, SecondGenome, BestGenome]
		self.MutationProbability = 1.0/(Amount * len(alleleGroups))
		self.Lgroups = [[sgaLocus(algr) for algr in alleleGroups] for x in range(Amount)]
		# Initializing random generators
		self.randmut = random.Random()
		self.randsel = random.Random()
		self.randfrq = random.Random()
	
	# >>> private methods starts
	
	def __GenerateIndividual(self, GenomeNo):
		assert GenomeNo in [0,1]
		for group in self.Lgroups:
			for locus in group:
				al = None
				# Does mutation occur
				if self.randmut.random() < self.MutationProbability:
					al = self.randsel.choice(locus.Alleles.keys())
				# select allele by it`s frequency in genotype
				else:
					while al == None:
						for allele in locus.Alleles.keys():
							if self.randfrq.random() < locus.Alleles[allele]:
								al = allele
								break
				# allele is selected, now setting genome
				locus.Genes[GenomeNo] = al
				if locus.Genes[2] == None:
					locus.Genes[2] = al
	
	def __AffectAlleles(self, BetterGenome, UpdateBest):
		assert BetterGenome in [0,1]
		afirst  = self.AlleleAffectValue if BetterGenome == 0 else -self.AlleleAffectValue
		asecond = self.AlleleAffectValue if BetterGenome == 1 else -self.AlleleAffectValue
		
		for group in self.Lgroups:
			for locus in group:
				pfirst  = locus.Alleles[locus.Genes[0]] + afirst
				psecond = locus.Alleles[locus.Genes[1]] + asecond
				pfirst  = 1.0 if pfirst > 1.0  else 0.0 if pfirst < 0.0  else pfirst
				psecond = 1.0 if psecond > 1.0 else 0.0 if psecond < 0.0 else psecond
				locus.Alleles[locus.Genes[0]] = pfirst
				locus.Alleles[locus.Genes[1]] = psecond
				# check do we need to update best genome
				if UpdateBest:
					locus.Genes[2] = locus.Genes[BetterGenome]
	
	# <<< private methods ends
	
	def Evolve(self,cycles):
		for iter in range(cycles):
			BetterGenome, UpdateBest = None, False
			self.__GenerateIndividual(0)
			self.__GenerateIndividual(1)
			self.Fitness[0] = self.FitnessFunc(self,0)
			self.Fitness[1] = self.FitnessFunc(self,1)
			if self.Fitness[2] == None:
				self.Fitness[2] = self.FitnessFunc(self,2)
			
			if self.Fitness[0] > self.Fitness[1]:
				BetterGenome = 0 if not self.Minimize else 1
			elif self.Fitness[0] < self.Fitness[1]:
				BetterGenome = 1 if not self.Minimize else 0
			
			if BetterGenome != None:
				if (self.Fitness[BetterGenome] > self.Fitness[2] and not self.Minimize) or \
					(self.Fitness[BetterGenome] < self.Fitness[2] and self.Minimize):
						UpdateBest = True
						self.Fitness[2] = self.Fitness[BetterGenome]
				self.__AffectAlleles(BetterGenome,UpdateBest)
				if self.NotifyFunc and UpdateBest:
					self.NotifyFunc(self,iter)
	
	def DumpGenotype(self):
		for ixg,group in enumerate(self.Lgroups):
			for ixl,locus in enumerate(group):
				for ixa,allele in enumerate(locus.Alleles):
					print "Grp_"+str(ixg),"|","Loc_"+str(ixl),"|",allele,"=>",locus.Alleles[allele],"prob."

def testFitness(gen,n):
	# Try to find x,y,z such that equation x^2 - y^2 - z^2 - 27 = 0
	return abs(gen.Lgroups[0][0].Genes[n]**2-gen.Lgroups[0][1].Genes[n]**2-gen.Lgroups[0][2].Genes[n]**2-27)

def testNotify(gen,iter):
		print 'iteration_'+str(iter)+':   ','|'+str(gen.Lgroups[0][0].Genes[2])+'^2 - '+\
						str(gen.Lgroups[0][1].Genes[2])+'^2 - '+\
						str(gen.Lgroups[0][2].Genes[2])+'^2 - 27| =',gen.Fitness[2]

if __name__ == "__main__":
	print 'Solving equation x^2 - y^2 - z^2 - 27 = 0'
	print '--------------------------------------------'
	gen = sgaGenotype([range(2,61),range(2,61),range(2,61)], 1, testFitness, testNotify, Minimize = True)
	gen.Evolve(1000)
