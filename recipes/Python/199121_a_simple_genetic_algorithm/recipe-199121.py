#
# genetic.py
#

import random

MAXIMIZE, MINIMIZE = 11, 22

class Individual(object):
    alleles = (0,1)
    length = 30
    seperator = ''
    optimization = MINIMIZE

    def __init__(self, chromosome=None):
        self.chromosome = chromosome or self._makechromosome()
        self.score = None  # set during evaluation
    
    def _makechromosome(self):
        "makes a chromosome from randomly selected alleles."
        return [random.choice(self.alleles) for gene in range(self.length)]

    def evaluate(self, optimum=None):
        "this method MUST be overridden to evaluate individual fitness score."
        pass
    
    def crossover(self, other):
        "override this method to use your preferred crossover method."
        return self._twopoint(other)
    
    def mutate(self, gene):
        "override this method to use your preferred mutation method."
        self._pick(gene) 
    
    # sample mutation method
    def _pick(self, gene):
        "chooses a random allele to replace this gene's allele."
        self.chromosome[gene] = random.choice(self.alleles)
    
    # sample crossover method
    def _twopoint(self, other):
        "creates offspring via two-point crossover between mates."
        left, right = self._pickpivots()
        def mate(p0, p1):
            chromosome = p0.chromosome[:]
            chromosome[left:right] = p1.chromosome[left:right]
            child = p0.__class__(chromosome)
            child._repair(p0, p1)
            return child
        return mate(self, other), mate(other, self)

    # some crossover helpers ...
    def _repair(self, parent1, parent2):
        "override this method, if necessary, to fix duplicated genes."
        pass

    def _pickpivots(self):
        left = random.randrange(1, self.length-2)
        right = random.randrange(left, self.length-1)
        return left, right

    #
    # other methods
    #

    def __repr__(self):
        "returns string representation of self"
        return '<%s chromosome="%s" score=%s>' % \
               (self.__class__.__name__,
                self.seperator.join(map(str,self.chromosome)), self.score)

    def __cmp__(self, other):
        if self.optimization == MINIMIZE:
            return cmp(self.score, other.score)
        else: # MAXIMIZE
            return cmp(other.score, self.score)
    
    def copy(self):
        twin = self.__class__(self.chromosome[:])
        twin.score = self.score
        return twin


class Environment(object):
    def __init__(self, kind, population=None, size=100, maxgenerations=100, 
                 crossover_rate=0.90, mutation_rate=0.01, optimum=None):
        self.kind = kind
        self.size = size
        self.optimum = optimum
        self.population = population or self._makepopulation()
        for individual in self.population:
            individual.evaluate(self.optimum)
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.maxgenerations = maxgenerations
        self.generation = 0
        self.report()

    def _makepopulation(self):
        return [self.kind() for individual in range(self.size)]
    
    def run(self):
        while not self._goal():
            self.step()
    
    def _goal(self):
        return self.generation > self.maxgenerations or \
               self.best.score == self.optimum
    
    def step(self):
        self.population.sort()
        self._crossover()
        self.generation += 1
        self.report()
    
    def _crossover(self):
        next_population = [self.best.copy()]
        while len(next_population) < self.size:
            mate1 = self._select()
            if random.random() < self.crossover_rate:
                mate2 = self._select()
                offspring = mate1.crossover(mate2)
            else:
                offspring = [mate1.copy()]
            for individual in offspring:
                self._mutate(individual)
                individual.evaluate(self.optimum)
                next_population.append(individual)
        self.population = next_population[:self.size]

    def _select(self):
        "override this to use your preferred selection method"
        return self._tournament()
    
    def _mutate(self, individual):
        for gene in range(individual.length):
            if random.random() < self.mutation_rate:
                individual.mutate(gene)

    #
    # sample selection method
    #
    def _tournament(self, size=8, choosebest=0.90):
        competitors = [random.choice(self.population) for i in range(size)]
        competitors.sort()
        if random.random() < choosebest:
            return competitors[0]
        else:
            return random.choice(competitors[1:])
    
    def best():
        doc = "individual with best fitness score in population."
        def fget(self):
            return self.population[0]
        return locals()
    best = property(**best())

    def report(self):
        print "="*70
        print "generation: ", self.generation
        print "best:       ", self.best



---------------------------------------------------------------------
#
# onemax.py - useage example
#
# the fittest individual will have a chromosome consisting of 30 '1's
#

import genetic

class OneMax(genetic.Individual):
    optimization = genetic.MAXIMIZE 
    def evaluate(self, optimum=None):
        self.score = sum(self.chromosome)
    def mutate(self, gene):
        self.chromosome[gene] = not self.chromosome[gene] # bit flip
   
if __name__ == "__main__":
    env = genetic.Environment(OneMax, maxgenerations=1000, optimum=30)
    env.run()
