# Author: James Collins

# Purpose: To allocate shares of cost amongst

# a group of friends who benifit by mutual cooperation.



from __future__ import division

from random import randint

from math import factorial

from copy import copy



# Travelling salesman solver

# global variables for tsp

qstart = 0 

qend = 0

queue = []

bestCost = 0

bestTrack = ''

def tsp(nodes, start):

    global qstart

    global qend

    global queue

    global bestCost

    global bestTrack

    n = len(nodes)

    if n == 0:

        return [], 0

    qstart = 0

    qend = n - 1

    queue   = copy(nodes) #range(n)

    bestCost = 9999999 # a very large number

    bestTrack = ''

    def recur(head, last, CostSoFar, track):

        global bestCost

        global bestTrack

        for j in  range( n-head):

            node = gett()

            track2 = track + node.initial

            NewCost = CostSoFar + metric(last, node)

            if NewCost < bestCost:

                if head < n-2:

                   recur(head+1, node, NewCost, track2)

                else:

                    node2 = gett()

                    finalCost = NewCost + metric(node, node2)

                    if finalCost < bestCost:

                        bestCost = finalCost

                        bestTrack = track2 + node2.initial

                    putt(node2)

            putt(node)

    def gett():

        global qstart

        x = queue[qstart]

        qstart += 1

        if qstart == n:

           qstart = 0

        return x

    def putt(x):

        global queue

        global qend

        qend += 1

        if qend == n:

           qend = 0

        queue[qend] = x

    recur(0, start, 0, '') # exhaustive search of all permutations

    return bestTrack, bestCost



# MAIN PROGRAM

people = []

class person:

    def __init__(self, name, x, y):

        self.name     = name

        self.initial  = name[0]

        self.x        = x # house location North/South

        self.y        = y # house location East/West

        self.bitplace = pow(2, len(people))

    def isElementOf(self, n): # If the ith bit in the index of

        # powerset (base 2)is 1 then it contains the ith person,

        # or else it dosnt.                

        if self.bitplace & n <> 0:

           return True

        return False                



def metric(a,b): # city grid

    return abs(a.x - b.x) + abs(a.y - b.y)



   

# random locations are being used for test purposes.

# Cost of travel is asssumed to be proportional to distance



pub = person('Shakespear', 5, 5)

people.append(person('Anne',   randint(1, 10), randint(1, 10)))

people.append(person('Brian',  randint(1, 10), randint(1, 10)))

people.append(person('Cindy',  randint(1, 10), randint(1, 10)))

people.append(person('David',  randint(1, 10), randint(1, 10)))

people.append(person('Elaine', randint(1, 10), randint(1, 10)))

#people.append(person('Francis', randint(1, 10), randint(1, 10)))

#people.append(person('Girlee', randint(1, 10), randint(1, 10)))

#people.append(person('Him', randint(1, 10), randint(1, 10)))

#people.append(person('Indy', randint(1, 10), randint(1, 10)))

#people.append(person('Jim', randint(1, 10), randint(1, 10)))

#people.append(person('Kathy', randint(1, 10), randint(1, 10))) # On my 3Gz Dual Core this takes 3min, mostly solving tsp



lenPeople = len(people)

class solution:

    def __init__(self, coalition):

        self.coalition = coalition

        self.size   = len(coalition)

        self.index  = len(powerset)

        self.split  = []

        if len(coalition) == 1: # individual

            self.cost = metric(coalition[0], pub)

            self.trk  = coalition[0].initial

            coalition[0].cost = self.cost

        else:

            self.trk, self.cost = tsp(coalition, pub)

        print 'route: ', self.trk, 'cost>',self.cost



powerset = []

# The size of the problem increases exponentialy

# w.r.t the number of people.

# Fortunately only about four people can fit in a taxi.

for i in range(pow(2, lenPeople)): # itterating over the power set

    newset = []

    for j in people:

        if j.isElementOf(i):

            newset.append(j)

    powerset.append(solution(newset))



def ShapleySub(q, p, setindex, personbit):

    s = q.size

    t = factorial(s) * factorial(lenPeople - s - 1)

    v = powerset[setindex + personbit]

    return t * ( v.cost - q.cost)

# Note: The Shapley value method assumes that there is no

# incentive for any party to defect from the grand

# coalition. This may not be true in this scenario as it

# may be more efficient for parties to travel seperately.

# In this aproach I calculate the minimum possible cost for the grand coalition

# allowing for seperate taxi travel and assign cost portions to each person

# as if there were no strategic politicing.

# For example if A can travel with B or C, but

# A, B and C cannot travel together. Both B and C are advantaged and A pays less

# than choosing to travel with either. So even if B ends up travelling home alone

# his travel is discounted by the others because of his ability to dispute

# the status quoe.



# test if union cost > sum cost of partitions

for setSize in range(2, lenPeople + 1):

    for p in powerset:

        if p.size == setSize:

            for i in range(1, pow(2, p.size-1)): # itterating all possible splits

                subset0s = 0

                subset1s = 0

                for j in range(p.size):

                    k = pow(2, j)

                    if k & i == 0: # note this coresponds to the bit places of the coalition not to the people list.

                       subset0s += p.coalition[j].bitplace # bitplace coresponds to the people list

                    else:

                       subset1s += p.coalition[j].bitplace

                if powerset[subset0s].cost + powerset[subset1s].cost < p.cost:

                   # subsets gain more by travelling seperately

                   print 'New costing for', p.trk, powerset[subset0s].cost + powerset[subset1s].cost, 'down from', p.cost

                   p.cost = powerset[subset0s].cost + powerset[subset1s].cost

                   p.split = [subset0s, subset1s]



                            

print 'Shapley values'

for p in people:

    Shapley = 0.0

    personbit = p.bitplace

    for q in powerset:

        setindex = q.index

        if not(p.isElementOf( setindex)):

            Shapley += ShapleySub(q, p, setindex, personbit)

    Shapley = Shapley / factorial(lenPeople)

    diff = p.cost - Shapley

    if p.cost > 0:

        perc = int(diff / p.cost * 100)

    else:

        perc = 0

    print "%s pays %6.2f saves %6.2f saving %d percent." %(p.name, Shapley, diff, perc) 



# Draws map

print

print '#######################'

for i in range(1, 11):

    line = '# '

    for j in range(1, 11):

         match = False 

         if i == pub.x and j == pub.y:

             line += pub.initial

             match = True

         for p in people:

             if p.x == i and p.y == j:

                 line += p.initial

                 match = True

         if not match:

             line += '. '

         else:

             line += ' '

    line += '#'

    print line

print '#######################'    



def AllocateTaxis(pset):

    if len(pset.split) == 0:

       print pset.trk, pset.cost

    else:

       AllocateTaxis(powerset[pset.split[0]])

       AllocateTaxis(powerset[pset.split[1]])

print

print 'Allocating taxis'

AllocateTaxis(powerset[len(powerset)-1])
