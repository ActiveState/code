#http://en.wikipedia.org/wiki/Partition_problem
import random
import logging
logging.basicConfig(level = logging.DEBUG)
log = logging.getLogger('partitionselection')
CROSSOVER_FRACTION = 0.20
SELECTIVE_FRACTION = 0.50
VARIANTS = 5
POPULATION_SIZE = 20
ITERATIONS = 100

def crossover(a,b):
    ml = min([len(a), len(b)])
    used_indices = []
    for i in range(0, int(ml*CROSSOVER_FRACTION)): 
        ra = random.randint(0,ml-1)
        while ra in used_indices:
            ra = random.randint(0,ml-1)
        a[ra], b[ra] = b[ra], a[ra]
        used_indices.append(ra)
    return (abs(sum(a)-sum(b)), a, b)

def naturalselection(partition_traids):
    global least_diff
    new_partition_traids = partition_traids [:]
    for partition_traid in partition_traids:
        for i in range(VARIANTS):
            variant = crossover(*partition_traid[1:])
            if variant[0]<least_diff:
                new_partition_traids.append(variant)
    new_partition_traids.sort()
    least_diff = new_partition_traids[0][0]
    remaining_partition_triads = new_partition_traids\
        [:int(POPULATION_SIZE*SELECTIVE_FRACTION)]
    return remaining_partition_triads
                     
if __name__ == '__main__':
    least_diff = 99999999
    import simplejson
    #assumes that the file named "population" has the raw 
    #population, a python list dumped with simplejson
    population = simplejson.loads(file('population').read())
    n = len(population)
    partition_a, partition_b = population[:n/2], population[n/2:]
    partition_traids = [(abs(sum(partition_a)-sum(partition_b)), partition_a, partition_b)]
    for i in range(ITERATIONS):
        partition_traids = naturalselection(partition_traids)
    print least_diff, partition_traids[0]
