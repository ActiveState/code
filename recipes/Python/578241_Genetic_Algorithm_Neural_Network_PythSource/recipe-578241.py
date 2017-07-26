from operator import itemgetter, attrgetter
import math
import random
import string
import timeit
from timeit import Timer as t
import matplotlib.pyplot as plt
import numpy as np

def sigmoid (x):
  return math.tanh(x)

def makeMatrix ( I, J, fill=0.0):
  m = []
  for i in range(I):
    m.append([fill]*J)
  return m
  
def randomizeMatrix ( matrix, a, b):
  for i in range ( len (matrix) ):
    for j in range ( len (matrix[0]) ):
      matrix[i][j] = random.uniform(a,b)

class NN:
  def __init__(self, NI, NH, NO):
    self.ni = NI
    self.nh = NH
    self.no = NO
    self.ai = [1.0]*self.ni
    self.ah = [1.0]*self.nh
    self.ao = [1.0]*self.no
    self.wi = [ [0.0]*self.nh for i in range(self.ni) ]
    self.wo = [ [0.0]*self.no for j in range(self.nh) ]
    randomizeMatrix ( self.wi, -0.2, 0.2 )
    randomizeMatrix ( self.wo, -2.0, 2.0 )

  def runNN (self, inputs):
    if len(inputs) != self.ni:
      print 'incorrect number of inputs'
    for i in range(self.ni):
      self.ai[i] = inputs[i]
    for j in range(self.nh):
      self.ah[j] = sigmoid(sum([ self.ai[i]*self.wi[i][j] for i in range(self.ni) ]))
    for k in range(self.no):
      self.ao[k] = sigmoid(sum([ self.ah[j]*self.wo[j][k] for j in range(self.nh) ]))
    return self.ao

  def weights(self):
    print 'Input weights:'
    for i in range(self.ni):
      print self.wi[i]
    print
    print 'Output weights:'
    for j in range(self.nh):
      print self.wo[j]
    print ''

  def test(self, patterns):
    results, targets = [], []
    for p in patterns:
      inputs = p[0]
      rounded = [ round(i) for i in self.runNN(inputs) ]
      if rounded == p[1]: result = '+++++'
      else: result = '-----'
      print '%s %s %s %s %s %s %s' %( 'Inputs:', p[0], '-->', str(self.runNN(inputs)).rjust(65), 'Target', p[1], result)
      results+= self.runNN(inputs)
      targets += p[1]
    return results, targets

  def sumErrors (self):
    error = 0.0
    for p in pat:
      inputs = p[0]
      targets = p[1]
      self.runNN(inputs)
      error += self.calcError(targets)
    inverr = 1.0/error
    return inverr

  def calcError (self, targets):
    error = 0.0
    for k in range(len(targets)):
      error += 0.5 * (targets[k]-self.ao[k])**2
    return error

  def assignWeights (self, weights, I):
    io = 0
    for i in range(self.ni):
      for j in range(self.nh):
        self.wi[i][j] = weights[I][io][i][j]
    io = 1
    for j in range(self.nh):
      for k in range(self.no):
        self.wo[j][k] = weights[I][io][j][k]

  def testWeights (self, weights, I):
    same = []
    io = 0
    for i in range(self.ni):
      for j in range(self.nh):
        if self.wi[i][j] != weights[I][io][i][j]:
          same.append(('I',i,j, round(self.wi[i][j],2),round(weights[I][io][i][j],2),round(self.wi[i][j] - weights[I][io][i][j],2)))

    io = 1
    for j in range(self.nh):
      for k in range(self.no):
        if self.wo[j][k] !=  weights[I][io][j][k]:
          same.append((('O',j,k), round(self.wo[j][k],2),round(weights[I][io][j][k],2),round(self.wo[j][k] - weights[I][io][j][k],2)))
    if same != []:
      print same

def roulette (fitnessScores):
  cumalativeFitness = 0.0
  r = random.random()
  for i in range(len(fitnessScores)): 
    cumalativeFitness += fitnessScores[i]
    if cumalativeFitness > r: 
      return i
      
def calcFit (numbers):  # each fitness is a fraction of the total error
  total, fitnesses = sum(numbers), []
  for i in range(len(numbers)):           
    fitnesses.append(numbers[i]/total)
  return fitnesses

# takes a population of NN objects
def pairPop (pop):
  weights, errors = [], []
  for i in range(len(pop)):                 # for each individual
    weights.append([pop[i].wi,pop[i].wo])   # append input & output weights of individual to list of all pop weights
    errors.append(pop[i].sumErrors())       # append 1/sum(MSEs) of individual to list of pop errors
  fitnesses = calcFit(errors)               # fitnesses are a fraction of the total error
  for i in range(int(pop_size*0.15)): 
    print str(i).zfill(2), '1/sum(MSEs)', str(errors[i]).rjust(15), str(int(errors[i]*graphical_error_scale)*'-').rjust(20), 'fitness'.rjust(12), str(fitnesses[i]).rjust(17), str(int(fitnesses[i]*1000)*'-').rjust(20)
  del pop
  return zip(weights, errors,fitnesses)            # weights become item[0] and fitnesses[1] in this way fitness is paired with its weight in a tuple
  
def rankPop (newpopW,pop):
  errors, copy = [], []           # a fresh pop of NN's are assigned to a list of len pop_size
  #pop = [NN(ni,nh,no)]*pop_size # this does not work as they are all copies of eachother
  pop = [NN(ni,nh,no) for i in range(pop_size) ]
  for i in range(pop_size): copy.append(newpopW[i])
  for i in range(pop_size):  
    pop[i].assignWeights(newpopW, i)                                    # each individual is assigned the weights generated from previous iteration
    pop[i].testWeights(newpopW, i)
  for i in range(pop_size):  
    pop[i].testWeights(newpopW, i)
  pairedPop = pairPop(pop)                                              # the fitness of these weights is calculated and tupled with the weights
  rankedPop = sorted(pairedPop, key = itemgetter(-1), reverse = True)   # weights are sorted in descending order of fitness (fittest first)
  errors = [ eval(repr(x[1])) for x in rankedPop ]
  return rankedPop, eval(repr(rankedPop[0][1])), float(sum(errors))/float(len(errors))

def iteratePop (rankedPop):
  rankedWeights = [ item[0] for item in rankedPop]
  fitnessScores = [ item[-1] for item in rankedPop]
  newpopW = [ eval(repr(x)) for x in rankedWeights[:int(pop_size*0.15)] ]
  while len(newpopW) <= pop_size:                                       # Breed two randomly selected but different chromos until pop_size reached
    ch1, ch2 = [], []
    index1 = roulette(fitnessScores)                                    
    index2 = roulette(fitnessScores)
    while index1 == index2:                                             # ensures different chromos are used for breeeding 
      index2 = roulette(fitnessScores)
    #index1, index2 = 3,4
    ch1.extend(eval(repr(rankedWeights[index1])))
    ch2.extend(eval(repr(rankedWeights[index2])))
    if random.random() < crossover_rate: 
      ch1, ch2 = crossover(ch1, ch2)
    mutate(ch1)
    mutate(ch2)
    newpopW.append(ch1)
    newpopW.append(ch2)
  return newpopW

graphical_error_scale = 100
max_iterations = 4000
pop_size = 100
mutation_rate = 0.1
crossover_rate = 0.8
ni, nh, no = 4,6,1

def main ():
  # Rank first random population
  pop = [ NN(ni,nh,no) for i in range(pop_size) ] # fresh pop
  pairedPop = pairPop(pop)
  rankedPop = sorted(pairedPop, key = itemgetter(-1), reverse = True) # THIS IS CORRECT
  # Keep iterating new pops until max_iterations
  iters = 0
  tops, avgs = [], []
  while iters != max_iterations:
    if iters%1 == 0:
      print 'Iteration'.rjust(150), iters
    newpopW = iteratePop(rankedPop)
    rankedPop, toperr, avgerr = rankPop(newpopW,pop)
    tops.append(toperr)
    avgs.append(avgerr)
    iters+=1
  
  # test a NN with the fittest weights
  tester = NN (ni,nh,no)
  fittestWeights = [ x[0] for x in rankedPop ]
  tester.assignWeights(fittestWeights, 0)
  results, targets = tester.test(testpat)
  x = np.arange(0,150)
  title2 = 'Test after '+str(iters)+' iterations'
  plt.title(title2)
  plt.ylabel('Node output')
  plt.xlabel('Instances')
  plt.plot( results, 'xr', linewidth = 0.5)
  plt.plot( targets, 's', color = 'black',linewidth = 3)
  #lines = plt.plot( results, 'sg')
  plt.annotate(s='Target Values', xy = (110, 0),color = 'black', family = 'sans-serif', size  ='small')
  plt.annotate(s='Test Values', xy = (110, 0.5),color = 'red', family = 'sans-serif', size  ='small', weight = 'bold')
  plt.figure(2)
  plt.subplot(121)
  plt.title('Top individual error evolution')
  plt.ylabel('Inverse error')
  plt.xlabel('Iterations')
  plt.plot( tops, '-g', linewidth = 1)
  plt.subplot(122)
  plt.plot( avgs, '-g', linewidth = 1)
  plt.title('Population average error evolution')
  plt.ylabel('Inverse error')
  plt.xlabel('Iterations')
  
  plt.show()
  
  print 'max_iterations',max_iterations,'\tpop_size',pop_size,'pop_size*0.15',int(pop_size*0.15),'\tmutation_rate',mutation_rate,'crossover_rate',crossover_rate,'ni, nh, no',ni, nh, no

def crossover (m1, m2):
  r = random.randint(0, (ni*nh)+(nh*no) ) # ni*nh+nh*no  = total weights
  output1 = [ [[0.0]*nh]*ni ,[[0.0]*no]*nh ]
  output2 = [ [[0.0]*nh]*ni ,[[0.0]*no]*nh ]
  for i in range(len(m1)):
    for j in range(len(m1[i])):
      for k in range(len(m1[i][j])):
        if r >= 0:
          output1[i][j][k] = m1[i][j][k]
          output2[i][j][k] = m2[i][j][k]
        elif r < 0:
          output1[i][j][k] = m2[i][j][k]
          output2[i][j][k] = m1[i][j][k]
        r -=1
  return output1, output2

def mutate (m):
  # could include a constant to control 
  # how much the weight is mutated by
  for i in range(len(m)):
    for j in range(len(m[i])):
      for k in range(len(m[i][j])):
        if random.random() < mutation_rate:
            m[i][j][k] = random.uniform(-2.0,2.0)
  
if __name__ == "__main__":
    main()
pat = [
  [[5.1, 3.5, 1.4, 0.2], [-1], ['Iris-setosa']] ,
  [[4.9, 3.0, 1.4, 0.2], [-1], ['Iris-setosa']] ,
  [[4.7, 3.2, 1.3, 0.2], [-1], ['Iris-setosa']] ,
  [[5.4, 3.9, 1.7, 0.4], [-1], ['Iris-setosa']] ,
  [[4.6, 3.4, 1.4, 0.3], [-1], ['Iris-setosa']] ,
  [[5.0, 3.4, 1.5, 0.2], [-1], ['Iris-setosa']] ,
  [[4.4, 2.9, 1.4, 0.2], [-1], ['Iris-setosa']] ,
  [[4.9, 3.1, 1.5, 0.1], [-1], ['Iris-setosa']] ,
  [[5.4, 3.7, 1.5, 0.2], [-1], ['Iris-setosa']] ,
  [[4.8, 3.4, 1.6, 0.2], [-1], ['Iris-setosa']] ,
  [[4.8, 3.0, 1.4, 0.1], [-1], ['Iris-setosa']] ,
  [[4.3, 3.0, 1.1, 0.1], [-1], ['Iris-setosa']] ,
  [[5.8, 4.0, 1.2, 0.2], [-1], ['Iris-setosa']] ,
  [[5.7, 4.4, 1.5, 0.4], [-1], ['Iris-setosa']] ,
  [[5.4, 3.9, 1.3, 0.4], [-1], ['Iris-setosa']] ,
  [[5.1, 3.5, 1.4, 0.3], [-1], ['Iris-setosa']] ,
  [[5.7, 3.8, 1.7, 0.3], [-1], ['Iris-setosa']] ,
  [[5.1, 3.8, 1.5, 0.3], [-1], ['Iris-setosa']] ,
  [[5.4, 3.4, 1.7, 0.2], [-1], ['Iris-setosa']] ,
  [[5.1, 3.7, 1.5, 0.4], [-1], ['Iris-setosa']] ,
  [[4.6, 3.6, 1.0, 0.2], [-1], ['Iris-setosa']] ,
  [[5.1, 3.3, 1.7, 0.5], [-1], ['Iris-setosa']] ,
  [[4.8, 3.4, 1.9, 0.2], [-1], ['Iris-setosa']] ,
  [[5.0, 3.0, 1.6, 0.2], [-1], ['Iris-setosa']] ,
  [[5.0, 3.4, 1.6, 0.4], [-1], ['Iris-setosa']] ,
  [[5.2, 3.5, 1.5, 0.2], [-1], ['Iris-setosa']] ,
  [[5.2, 3.4, 1.4, 0.2], [-1], ['Iris-setosa']] ,
  [[4.7, 3.2, 1.6, 0.2], [-1], ['Iris-setosa']] ,
  [[4.8, 3.1, 1.6, 0.2], [-1], ['Iris-setosa']] ,
  [[5.4, 3.4, 1.5, 0.4], [-1], ['Iris-setosa']] ,
  [[5.2, 4.1, 1.5, 0.1], [-1], ['Iris-setosa']] ,
  [[5.5, 4.2, 1.4, 0.2], [-1], ['Iris-setosa']] ,
  [[4.9, 3.1, 1.5, 0.1], [-1], ['Iris-setosa']] ,
  [[5.0, 3.2, 1.2, 0.2], [-1], ['Iris-setosa']] ,
  [[5.5, 3.5, 1.3, 0.2], [-1], ['Iris-setosa']] ,
  [[4.9, 3.1, 1.5, 0.1], [-1], ['Iris-setosa']] ,
  [[4.4, 3.0, 1.3, 0.2], [-1], ['Iris-setosa']] ,
  [[5.1, 3.4, 1.5, 0.2], [-1], ['Iris-setosa']] ,
  [[5.0, 3.5, 1.3, 0.3], [-1], ['Iris-setosa']] ,
  [[4.5, 2.3, 1.3, 0.3], [-1], ['Iris-setosa']] ,
  [[4.4, 3.2, 1.3, 0.2], [-1], ['Iris-setosa']] ,
  [[5.0, 3.5, 1.6, 0.6], [-1], ['Iris-setosa']] ,
  [[5.1, 3.8, 1.9, 0.4], [-1], ['Iris-setosa']] ,
  [[4.8, 3.0, 1.4, 0.3], [-1], ['Iris-setosa']] ,
  [[5.1, 3.8, 1.6, 0.2], [-1], ['Iris-setosa']] ,
  [[4.6, 3.2, 1.4, 0.2], [-1], ['Iris-setosa']] ,
  [[5.3, 3.7, 1.5, 0.2], [-1], ['Iris-setosa']] ,
  [[5.0, 3.3, 1.4, 0.2], [-1], ['Iris-setosa']] ,
  [[7.0, 3.2, 4.7, 1.4], [0], ['Iris-versicolor']] ,
  [[6.4, 3.2, 4.5, 1.5], [0], ['Iris-versicolor']] ,
  [[6.9, 3.1, 4.9, 1.5], [0], ['Iris-versicolor']] ,
  [[5.5, 2.3, 4.0, 1.3], [0], ['Iris-versicolor']] ,
  [[6.5, 2.8, 4.6, 1.5], [0], ['Iris-versicolor']] ,
  [[5.7, 2.8, 4.5, 1.3], [0], ['Iris-versicolor']] ,
  [[6.3, 3.3, 4.7, 1.6], [0], ['Iris-versicolor']] ,
  [[4.9, 2.4, 3.3, 1.0], [0], ['Iris-versicolor']] ,
  [[6.6, 2.9, 4.6, 1.3], [0], ['Iris-versicolor']] ,
  [[5.2, 2.7, 3.9, 1.4], [0], ['Iris-versicolor']] ,
  [[5.0, 2.0, 3.5, 1.0], [0], ['Iris-versicolor']] ,
  [[5.9, 3.0, 4.2, 1.5], [0], ['Iris-versicolor']] ,
  [[6.0, 2.2, 4.0, 1.0], [0], ['Iris-versicolor']] ,
  [[6.1, 2.9, 4.7, 1.4], [0], ['Iris-versicolor']] ,
  [[5.6, 2.9, 3.6, 1.3], [0], ['Iris-versicolor']] ,
  [[6.7, 3.1, 4.4, 1.4], [0], ['Iris-versicolor']] ,
  [[5.6, 3.0, 4.5, 1.5], [0], ['Iris-versicolor']] ,
  [[5.8, 2.7, 4.1, 1.0], [0], ['Iris-versicolor']] ,
  [[6.2, 2.2, 4.5, 1.5], [0], ['Iris-versicolor']] ,
  [[5.6, 2.5, 3.9, 1.1], [0], ['Iris-versicolor']] ,
  [[5.9, 3.2, 4.8, 1.8], [0], ['Iris-versicolor']] ,
  [[6.1, 2.8, 4.0, 1.3], [0], ['Iris-versicolor']] ,
  [[6.3, 2.5, 4.9, 1.5], [0], ['Iris-versicolor']] ,
  [[6.1, 2.8, 4.7, 1.2], [0], ['Iris-versicolor']] ,
  [[6.4, 2.9, 4.3, 1.3], [0], ['Iris-versicolor']] ,
  [[6.6, 3.0, 4.4, 1.4], [0], ['Iris-versicolor']] ,
  [[6.8, 2.8, 4.8, 1.4], [0], ['Iris-versicolor']] ,
  [[6.7, 3.0, 5.0, 1.7], [0], ['Iris-versicolor']] ,
  [[6.0, 2.9, 4.5, 1.5], [0], ['Iris-versicolor']] ,
  [[5.7, 2.6, 3.5, 1.0], [0], ['Iris-versicolor']] ,
  [[5.5, 2.4, 3.8, 1.1], [0], ['Iris-versicolor']] ,
  [[5.5, 2.4, 3.7, 1.0], [0], ['Iris-versicolor']] ,
  [[5.8, 2.7, 3.9, 1.2], [0], ['Iris-versicolor']] ,
  [[6.0, 2.7, 5.1, 1.6], [0], ['Iris-versicolor']] ,
  [[5.4, 3.0, 4.5, 1.5], [0], ['Iris-versicolor']] ,
  [[6.0, 3.4, 4.5, 1.6], [0], ['Iris-versicolor']] ,
  [[6.7, 3.1, 4.7, 1.5], [0], ['Iris-versicolor']] ,
  [[6.3, 2.3, 4.4, 1.3], [0], ['Iris-versicolor']] ,
  [[5.6, 3.0, 4.1, 1.3], [0], ['Iris-versicolor']] ,
  [[6.1, 3.0, 4.6, 1.4], [0], ['Iris-versicolor']] ,
  [[5.8, 2.6, 4.0, 1.2], [0], ['Iris-versicolor']] ,
  [[5.0, 2.3, 3.3, 1.0], [0], ['Iris-versicolor']] ,
  [[5.6, 2.7, 4.2, 1.3], [0], ['Iris-versicolor']] ,
  [[5.7, 3.0, 4.2, 1.2], [0], ['Iris-versicolor']] ,
  [[5.7, 2.9, 4.2, 1.3], [0], ['Iris-versicolor']] ,
  [[6.2, 2.9, 4.3, 1.3], [0], ['Iris-versicolor']] ,
  [[5.1, 2.5, 3.0, 1.1], [0], ['Iris-versicolor']] ,
  [[5.7, 2.8, 4.1, 1.3], [0], ['Iris-versicolor']] ,
  [[6.3, 3.3, 6.0, 2.5], [1], ['Iris-virginica']] ,
  [[5.8, 2.7, 5.1, 1.9], [1], ['Iris-virginica']] ,
  [[7.1, 3.0, 5.9, 2.1], [1], ['Iris-virginica']] ,
  [[6.3, 2.9, 5.6, 1.8], [1], ['Iris-virginica']] ,
  [[6.5, 3.0, 5.8, 2.2], [1], ['Iris-virginica']] ,
  [[7.6, 3.0, 6.6, 2.1], [1], ['Iris-virginica']] ,
  [[4.9, 2.5, 4.5, 1.7], [1], ['Iris-virginica']] ,
  [[7.3, 2.9, 6.3, 1.8], [1], ['Iris-virginica']] ,
  [[6.7, 2.5, 5.8, 1.8], [1], ['Iris-virginica']] ,
  [[7.2, 3.6, 6.1, 2.5], [1], ['Iris-virginica']] ,
  [[6.5, 3.2, 5.1, 2.0], [1], ['Iris-virginica']] ,
  [[6.4, 2.7, 5.3, 1.9], [1], ['Iris-virginica']] ,
  [[6.8, 3.0, 5.5, 2.1], [1], ['Iris-virginica']] ,
  [[5.7, 2.5, 5.0, 2.0], [1], ['Iris-virginica']] ,
  [[5.8, 2.8, 5.1, 2.4], [1], ['Iris-virginica']] ,
  [[7.7, 3.8, 6.7, 2.2], [1], ['Iris-virginica']] ,
  [[7.7, 2.6, 6.9, 2.3], [1], ['Iris-virginica']] ,
  [[6.0, 2.2, 5.0, 1.5], [1], ['Iris-virginica']] ,
  [[6.9, 3.2, 5.7, 2.3], [1], ['Iris-virginica']] ,
  [[5.6, 2.8, 4.9, 2.0], [1], ['Iris-virginica']] ,
  [[7.7, 2.8, 6.7, 2.0], [1], ['Iris-virginica']] ,
  [[6.3, 2.7, 4.9, 1.8], [1], ['Iris-virginica']] ,
  [[6.7, 3.3, 5.7, 2.1], [1], ['Iris-virginica']] ,
  [[7.2, 3.2, 6.0, 1.8], [1], ['Iris-virginica']] ,
  [[6.2, 2.8, 4.8, 1.8], [1], ['Iris-virginica']] ,
  [[6.1, 3.0, 4.9, 1.8], [1], ['Iris-virginica']] ,
  [[6.4, 2.8, 5.6, 2.1], [1], ['Iris-virginica']] ,
  [[7.2, 3.0, 5.8, 1.6], [1], ['Iris-virginica']] ,
  [[7.4, 2.8, 6.1, 1.9], [1], ['Iris-virginica']] ,
  [[7.9, 3.8, 6.4, 2.0], [1], ['Iris-virginica']] ,
  [[6.4, 2.8, 5.6, 2.2], [1], ['Iris-virginica']] ,
  [[6.3, 2.8, 5.1, 1.5], [1], ['Iris-virginica']] ,
  [[6.1, 2.6, 5.6, 1.4], [1], ['Iris-virginica']] ,
  [[7.7, 3.0, 6.1, 2.3], [1], ['Iris-virginica']] ,
  [[6.3, 3.4, 5.6, 2.4], [1], ['Iris-virginica']] ,
  [[6.4, 3.1, 5.5, 1.8], [1], ['Iris-virginica']] ,
  [[6.0, 3.0, 4.8, 1.8], [1], ['Iris-virginica']] ,
  [[6.9, 3.1, 5.4, 2.1], [1], ['Iris-virginica']] ,
  [[6.7, 3.1, 5.6, 2.4], [1], ['Iris-virginica']] ,
  [[6.9, 3.1, 5.1, 2.3], [1], ['Iris-virginica']] ,
  [[5.8, 2.7, 5.1, 1.9], [1], ['Iris-virginica']] ,
  [[6.8, 3.2, 5.9, 2.3], [1], ['Iris-virginica']] ,
  [[6.7, 3.3, 5.7, 2.5], [1], ['Iris-virginica']] ,
  [[6.7, 3.0, 5.2, 2.3], [1], ['Iris-virginica']] ,
  [[6.3, 2.5, 5.0, 1.9], [1], ['Iris-virginica']] ,
  [[6.5, 3.0, 5.2, 2.0], [1], ['Iris-virginica']] ,
  [[6.2, 3.4, 5.4, 2.3], [1], ['Iris-virginica']] ,
  [[5.9, 3.0, 5.1, 1.8], [1], ['Iris-virginica']]
]

testpat = [
  [[5.1, 3.5, 1.4, 0.2], [-1], ['Iris-setosa']] ,
  [[4.9, 3.0, 1.4, 0.2], [-1], ['Iris-setosa']] ,
  [[4.7, 3.2, 1.3, 0.2], [-1], ['Iris-setosa']] ,
  [[5.4, 3.9, 1.7, 0.4], [-1], ['Iris-setosa']] ,
  [[4.6, 3.4, 1.4, 0.3], [-1], ['Iris-setosa']] ,
  [[5.0, 3.4, 1.5, 0.2], [-1], ['Iris-setosa']] ,
  [[4.4, 2.9, 1.4, 0.2], [-1], ['Iris-setosa']] ,
  [[4.9, 3.1, 1.5, 0.1], [-1], ['Iris-setosa']] ,
  [[5.4, 3.7, 1.5, 0.2], [-1], ['Iris-setosa']] ,
  [[4.8, 3.4, 1.6, 0.2], [-1], ['Iris-setosa']] ,
  [[4.8, 3.0, 1.4, 0.1], [-1], ['Iris-setosa']] ,
  [[4.3, 3.0, 1.1, 0.1], [-1], ['Iris-setosa']] ,
  [[5.8, 4.0, 1.2, 0.2], [-1], ['Iris-setosa']] ,
  [[5.7, 4.4, 1.5, 0.4], [-1], ['Iris-setosa']] ,
  [[5.4, 3.9, 1.3, 0.4], [-1], ['Iris-setosa']] ,
  [[5.1, 3.5, 1.4, 0.3], [-1], ['Iris-setosa']] ,
  [[5.7, 3.8, 1.7, 0.3], [-1], ['Iris-setosa']] ,
  [[5.1, 3.8, 1.5, 0.3], [-1], ['Iris-setosa']] ,
  [[5.4, 3.4, 1.7, 0.2], [-1], ['Iris-setosa']] ,
  [[5.1, 3.7, 1.5, 0.4], [-1], ['Iris-setosa']] ,
  [[4.6, 3.6, 1.0, 0.2], [-1], ['Iris-setosa']] ,
  [[5.1, 3.3, 1.7, 0.5], [-1], ['Iris-setosa']] ,
  [[4.8, 3.4, 1.9, 0.2], [-1], ['Iris-setosa']] ,
  [[5.0, 3.0, 1.6, 0.2], [-1], ['Iris-setosa']] ,
  [[5.0, 3.4, 1.6, 0.4], [-1], ['Iris-setosa']] ,
  [[5.2, 3.5, 1.5, 0.2], [-1], ['Iris-setosa']] ,
  [[5.2, 3.4, 1.4, 0.2], [-1], ['Iris-setosa']] ,
  [[4.7, 3.2, 1.6, 0.2], [-1], ['Iris-setosa']] ,
  [[4.8, 3.1, 1.6, 0.2], [-1], ['Iris-setosa']] ,
  [[5.4, 3.4, 1.5, 0.4], [-1], ['Iris-setosa']] ,
  [[5.2, 4.1, 1.5, 0.1], [-1], ['Iris-setosa']] ,
  [[5.5, 4.2, 1.4, 0.2], [-1], ['Iris-setosa']] ,
  [[4.9, 3.1, 1.5, 0.1], [-1], ['Iris-setosa']] ,
  [[5.0, 3.2, 1.2, 0.2], [-1], ['Iris-setosa']] ,
  [[5.5, 3.5, 1.3, 0.2], [-1], ['Iris-setosa']] ,
  [[4.9, 3.1, 1.5, 0.1], [-1], ['Iris-setosa']] ,
  [[4.4, 3.0, 1.3, 0.2], [-1], ['Iris-setosa']] ,
  [[5.1, 3.4, 1.5, 0.2], [-1], ['Iris-setosa']] ,
  [[5.0, 3.5, 1.3, 0.3], [-1], ['Iris-setosa']] ,
  [[4.5, 2.3, 1.3, 0.3], [-1], ['Iris-setosa']] ,
  [[4.4, 3.2, 1.3, 0.2], [-1], ['Iris-setosa']] ,
  [[5.0, 3.5, 1.6, 0.6], [-1], ['Iris-setosa']] ,
  [[5.1, 3.8, 1.9, 0.4], [-1], ['Iris-setosa']] ,
  [[4.8, 3.0, 1.4, 0.3], [-1], ['Iris-setosa']] ,
  [[5.1, 3.8, 1.6, 0.2], [-1], ['Iris-setosa']] ,
  [[4.6, 3.2, 1.4, 0.2], [-1], ['Iris-setosa']] ,
  [[5.3, 3.7, 1.5, 0.2], [-1], ['Iris-setosa']] ,
  [[5.0, 3.3, 1.4, 0.2], [-1], ['Iris-setosa']] ,
  [[7.0, 3.2, 4.7, 1.4], [0], ['Iris-versicolor']] ,
  [[6.4, 3.2, 4.5, 1.5], [0], ['Iris-versicolor']] ,
  [[6.9, 3.1, 4.9, 1.5], [0], ['Iris-versicolor']] ,
  [[5.5, 2.3, 4.0, 1.3], [0], ['Iris-versicolor']] ,
  [[6.5, 2.8, 4.6, 1.5], [0], ['Iris-versicolor']] ,
  [[5.7, 2.8, 4.5, 1.3], [0], ['Iris-versicolor']] ,
  [[6.3, 3.3, 4.7, 1.6], [0], ['Iris-versicolor']] ,
  [[4.9, 2.4, 3.3, 1.0], [0], ['Iris-versicolor']] ,
  [[6.6, 2.9, 4.6, 1.3], [0], ['Iris-versicolor']] ,
  [[5.2, 2.7, 3.9, 1.4], [0], ['Iris-versicolor']] ,
  [[5.0, 2.0, 3.5, 1.0], [0], ['Iris-versicolor']] ,
  [[5.9, 3.0, 4.2, 1.5], [0], ['Iris-versicolor']] ,
  [[6.0, 2.2, 4.0, 1.0], [0], ['Iris-versicolor']] ,
  [[6.1, 2.9, 4.7, 1.4], [0], ['Iris-versicolor']] ,
  [[5.6, 2.9, 3.6, 1.3], [0], ['Iris-versicolor']] ,
  [[6.7, 3.1, 4.4, 1.4], [0], ['Iris-versicolor']] ,
  [[5.6, 3.0, 4.5, 1.5], [0], ['Iris-versicolor']] ,
  [[5.8, 2.7, 4.1, 1.0], [0], ['Iris-versicolor']] ,
  [[6.2, 2.2, 4.5, 1.5], [0], ['Iris-versicolor']] ,
  [[5.6, 2.5, 3.9, 1.1], [0], ['Iris-versicolor']] ,
  [[5.9, 3.2, 4.8, 1.8], [0], ['Iris-versicolor']] ,
  [[6.1, 2.8, 4.0, 1.3], [0], ['Iris-versicolor']] ,
  [[6.3, 2.5, 4.9, 1.5], [0], ['Iris-versicolor']] ,
  [[6.1, 2.8, 4.7, 1.2], [0], ['Iris-versicolor']] ,
  [[6.4, 2.9, 4.3, 1.3], [0], ['Iris-versicolor']] ,
  [[6.6, 3.0, 4.4, 1.4], [0], ['Iris-versicolor']] ,
  [[6.8, 2.8, 4.8, 1.4], [0], ['Iris-versicolor']] ,
  [[6.7, 3.0, 5.0, 1.7], [0], ['Iris-versicolor']] ,
  [[6.0, 2.9, 4.5, 1.5], [0], ['Iris-versicolor']] ,
  [[5.7, 2.6, 3.5, 1.0], [0], ['Iris-versicolor']] ,
  [[5.5, 2.4, 3.8, 1.1], [0], ['Iris-versicolor']] ,
  [[5.5, 2.4, 3.7, 1.0], [0], ['Iris-versicolor']] ,
  [[5.8, 2.7, 3.9, 1.2], [0], ['Iris-versicolor']] ,
  [[6.0, 2.7, 5.1, 1.6], [0], ['Iris-versicolor']] ,
  [[5.4, 3.0, 4.5, 1.5], [0], ['Iris-versicolor']] ,
  [[6.0, 3.4, 4.5, 1.6], [0], ['Iris-versicolor']] ,
  [[6.7, 3.1, 4.7, 1.5], [0], ['Iris-versicolor']] ,
  [[6.3, 2.3, 4.4, 1.3], [0], ['Iris-versicolor']] ,
  [[5.6, 3.0, 4.1, 1.3], [0], ['Iris-versicolor']] ,
  [[6.1, 3.0, 4.6, 1.4], [0], ['Iris-versicolor']] ,
  [[5.8, 2.6, 4.0, 1.2], [0], ['Iris-versicolor']] ,
  [[5.0, 2.3, 3.3, 1.0], [0], ['Iris-versicolor']] ,
  [[5.6, 2.7, 4.2, 1.3], [0], ['Iris-versicolor']] ,
  [[5.7, 3.0, 4.2, 1.2], [0], ['Iris-versicolor']] ,
  [[5.7, 2.9, 4.2, 1.3], [0], ['Iris-versicolor']] ,
  [[6.2, 2.9, 4.3, 1.3], [0], ['Iris-versicolor']] ,
  [[5.1, 2.5, 3.0, 1.1], [0], ['Iris-versicolor']] ,
  [[5.7, 2.8, 4.1, 1.3], [0], ['Iris-versicolor']] ,
  [[6.3, 3.3, 6.0, 2.5], [1], ['Iris-virginica']] ,
  [[5.8, 2.7, 5.1, 1.9], [1], ['Iris-virginica']] ,
  [[7.1, 3.0, 5.9, 2.1], [1], ['Iris-virginica']] ,
  [[6.3, 2.9, 5.6, 1.8], [1], ['Iris-virginica']] ,
  [[6.5, 3.0, 5.8, 2.2], [1], ['Iris-virginica']] ,
  [[7.6, 3.0, 6.6, 2.1], [1], ['Iris-virginica']] ,
  [[4.9, 2.5, 4.5, 1.7], [1], ['Iris-virginica']] ,
  [[7.3, 2.9, 6.3, 1.8], [1], ['Iris-virginica']] ,
  [[6.7, 2.5, 5.8, 1.8], [1], ['Iris-virginica']] ,
  [[7.2, 3.6, 6.1, 2.5], [1], ['Iris-virginica']] ,
  [[6.5, 3.2, 5.1, 2.0], [1], ['Iris-virginica']] ,
  [[6.4, 2.7, 5.3, 1.9], [1], ['Iris-virginica']] ,
  [[6.8, 3.0, 5.5, 2.1], [1], ['Iris-virginica']] ,
  [[5.7, 2.5, 5.0, 2.0], [1], ['Iris-virginica']] ,
  [[5.8, 2.8, 5.1, 2.4], [1], ['Iris-virginica']] ,
  [[7.7, 3.8, 6.7, 2.2], [1], ['Iris-virginica']] ,
  [[7.7, 2.6, 6.9, 2.3], [1], ['Iris-virginica']] ,
  [[6.0, 2.2, 5.0, 1.5], [1], ['Iris-virginica']] ,
  [[6.9, 3.2, 5.7, 2.3], [1], ['Iris-virginica']] ,
  [[5.6, 2.8, 4.9, 2.0], [1], ['Iris-virginica']] ,
  [[7.7, 2.8, 6.7, 2.0], [1], ['Iris-virginica']] ,
  [[6.3, 2.7, 4.9, 1.8], [1], ['Iris-virginica']] ,
  [[6.7, 3.3, 5.7, 2.1], [1], ['Iris-virginica']] ,
  [[7.2, 3.2, 6.0, 1.8], [1], ['Iris-virginica']] ,
  [[6.2, 2.8, 4.8, 1.8], [1], ['Iris-virginica']] ,
  [[6.1, 3.0, 4.9, 1.8], [1], ['Iris-virginica']] ,
  [[6.4, 2.8, 5.6, 2.1], [1], ['Iris-virginica']] ,
  [[7.2, 3.0, 5.8, 1.6], [1], ['Iris-virginica']] ,
  [[7.4, 2.8, 6.1, 1.9], [1], ['Iris-virginica']] ,
  [[7.9, 3.8, 6.4, 2.0], [1], ['Iris-virginica']] ,
  [[6.4, 2.8, 5.6, 2.2], [1], ['Iris-virginica']] ,
  [[6.3, 2.8, 5.1, 1.5], [1], ['Iris-virginica']] ,
  [[6.1, 2.6, 5.6, 1.4], [1], ['Iris-virginica']] ,
  [[7.7, 3.0, 6.1, 2.3], [1], ['Iris-virginica']] ,
  [[6.3, 3.4, 5.6, 2.4], [1], ['Iris-virginica']] ,
  [[6.4, 3.1, 5.5, 1.8], [1], ['Iris-virginica']] ,
  [[6.0, 3.0, 4.8, 1.8], [1], ['Iris-virginica']] ,
  [[6.9, 3.1, 5.4, 2.1], [1], ['Iris-virginica']] ,
  [[6.7, 3.1, 5.6, 2.4], [1], ['Iris-virginica']] ,
  [[6.9, 3.1, 5.1, 2.3], [1], ['Iris-virginica']] ,
  [[5.8, 2.7, 5.1, 1.9], [1], ['Iris-virginica']] ,
  [[6.8, 3.2, 5.9, 2.3], [1], ['Iris-virginica']] ,
  [[6.7, 3.3, 5.7, 2.5], [1], ['Iris-virginica']] ,
  [[6.7, 3.0, 5.2, 2.3], [1], ['Iris-virginica']] ,
  [[6.3, 2.5, 5.0, 1.9], [1], ['Iris-virginica']] ,
  [[6.5, 3.0, 5.2, 2.0], [1], ['Iris-virginica']] ,
  [[6.2, 3.4, 5.4, 2.3], [1], ['Iris-virginica']] ,
  [[5.9, 3.0, 5.1, 1.8], [1], ['Iris-virginica']]
]
