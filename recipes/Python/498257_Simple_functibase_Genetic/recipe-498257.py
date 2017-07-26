from string import digits
from random import randrange, randint
try:
    import psyco
    psyco.full(memory=100)
    psyco.profile(0.05, memory=100)
    psyco.profile(0.2)
except:
    pass
operators = "+-*/"

genes = {
    0:'0',
    1:'1',
    2:'2',
    3:'3',
    4:'4',
    5:'5',
    6:'6',
    7:'7',
    8:'8',
    9:'9',
    10:'+',
    11:'-',
    12:'*',
    13:'/'
}

traits = {}
for key, value in enumerate(genes):
    traits[value] = key

def encode(expression):
    """Takes a mathmatic expression as a string and returns a chromosome."""
    output = []
    for char in expression:
        if char in traits.keys():
            output.append(traits[char])
    return output

def decode(chromosome):
    """Takes a chromosome (list) and returns an expression."""
    # this needs to be a mini state machine.
    # We expect a stream of number + operator pairs terminated with a number
    output = ""
    need_op = False
    for key in chromosome:
        gene = genes[key]
        if need_op:
            if gene in operators:
                output += gene
                need_op = False
            else:
                continue
        else:
            if gene in digits:
                output += gene
                need_op = True
            else:
                continue
    if not need_op:
        # we don't want an op hanging off the end
        output = output[:len(output)-1]
    return output

def makeChrom(length):
    """Create a random chromosome length long."""
    output = []
    for i in range(length):
        output.append(randrange(14))
    return output

def sortFitness(chromosomes, target):
    """Sort the chromosomes so the fitest comes first."""
    done = False
    fittest = []
    for chrom in chromosomes:
        # Decode
        pheno = decode(chrom)

        # Try to evaluate
        try:
            result = eval(pheno)
        except ZeroDivisionError:
            result = 0

        # Score based on result
        fit = abs(target-result)
        if fit == 0:
            done = True
            fit = -1
        print "%s =%s : %s" %(pheno.rjust(15), str(result).rjust(10),
                                      str(fit).rjust(15))
        fittest.append((fit, chrom))
    # Once we have a list of (fitness, chrom) pairs we can sort
    fittest.sort()
    return done, [item[-1] for item in fittest]
    

def breed(pop, number, mutation):
    """Breeds a population until there are 'number' of them."""
    output = pop[:] # carry over all the breeders
    while len(output) < number:
        # Create a new chromosome by crossing two random members
        child1, child2 = crossover(pop[randint(0, len(pop)-1)],
                                   pop[randint(0, len(pop)-1)],)
        child1 = mutate(child1, mutation)
        child2 = mutate(child2, mutation)
        output.extend([child1, child2])
    if len(output) > number:
        output[:number]
    return output

def crossover(chrom1, chrom2):
    """Cross two chromosomes."""
    breakpoint = randint(0, len(chrom1))
    return (chrom1[breakpoint:] + chrom2[:breakpoint],
            chrom2[breakpoint:] + chrom1[:breakpoint])

def mutate(chrom, rate=100):
    """Randomly mutate a chromosome.
    
    Rate is the chance in 100 that mutation will occure."""
    for i in range(len(chrom)):
        chance = randint(0, 100)
        if chance <= rate:
            chrom[i] = randint(0, 13)
    return chrom

def findFit(target=42, length=20, pop=20, mutation=1):
    """Evolve a population of math problems to solve for target."""
    population = [makeChrom(length) for i in range(pop)]
    generations = 0
    while True:
        print "Generation: %s" %generations
        print "%s%s%s" %("Chromosome".rjust(15), "Result".rjust(15),
                                      "Fitness".rjust(15))
        done, population = sortFitness(population, target)
        if not done:
            # take the first several fittest members
            fittest = population[:pop/4]
            # and breed them until you have a new population
            population = breed(fittest, pop, mutation)
        else:
            print "Solution found!"
            print "%s = %s" %(decode(population[0]), eval(decode(population[0]))),
            print "is the fitest solution for %s!" %target
            return generations, decode(population[0])
        generations += 1

do_average = False
if __name__ == "__main__":
    number = input("Enter a target number for the calculation: ")
    if do_average:
        results = []
        for i in range(50):
            generations, winner = findFit(target=number, pop=30, mutation=20)
            results.append((generations, winner))
        #results.sort()
        average = 0
        for item in results:
            average += item[0]
            print item[0], item[1]
        print "Average generations: %s" %average/50
    else:
        generations, winner = findFit(target=number, pop=30, mutation=20)
        print "Generations: %s, Winner: %s" %(generations, winner)
    raw_input("Press enter to continue...")
