"""
Artificial Neural Network 
"""

import numpy
import copy

def sigmoid(x):
	return 1.0/(1.0 + numpy.exp(-x))

class NeuralNet:

	def __init__(self, numUnitsPerLayer):
		"""
		Constructor
		@param numUnitsPerLayer numbers of units per layer, excluding bias
		"""

		numLayers = len(numUnitsPerLayer)
		if numLayers < 2:
			raise RuntimeError, 'ERROR number of layers must be >= 2! (Got %d)' % numLayers

		# total number of layers incl. input and output
		self.numLayers = numLayers 

		# activations
		self.activations = [ numpy.zeros( (numUnitsPerLayer[i] + 1,), numpy.float64 ) for i in range(numLayers)]

		# set the biases
		for el in range(numLayers):
			self.activations[el][0] = 1.0

		# weights
		self.weights = []
		self.bigDeltas = []
		self.approxGradients = []
		for el in range(numLayers - 1):
			shp = (numUnitsPerLayer[el+1], numUnitsPerLayer[el] + 1)
			self.weights.append( numpy.zeros(shp, numpy.float64) )
			self.bigDeltas.append( numpy.zeros(shp, numpy.float64) )
			self.approxGradients.append( numpy.zeros(shp, numpy.float64) )

		# back propagating errors, no error for layer 0
		self.deltas = [ numpy.zeros( (len(a)-1,), numpy.float64 ) for a in self.activations]
		self.deltas[0][:] = 0.0 # by definition

	def randomlyInitializeWeights(self, magnitude = 0.1):
		"""
		Randomly initialize the weights to values between -magnitude ... +magnitude
		@param magnitude
		"""
		numpy.random.seed(1234)
		for w in self.weights:
			w[:] = magnitude * (numpy.random.rand(w.shape[0], w.shape[1]) - 0.5)

	def forward(self, inputData):
		"""
		Compute activation by propagating input forward
		@param inputData input (excl. bias)
		"""
		self.activations[0][1:] = inputData # copy input data
		for el in range(1, self.numLayers):
			z = numpy.dot(self.weights[el-1], self.activations[el-1])
			self.activations[el][1:] = sigmoid(z)
			self.activations[el][0] = 1.0

		return self.getOutput()

	def backward(self, targetOutputData):
		"""
		Propagate error backward
		@param targetOutputData target output data
		"""
		weightsTranspose = [ numpy.transpose(w) for w in self.weights ]
		self.deltas[self.numLayers - 1][:] = self.activations[-1][1:] - targetOutputData
		for el in range(self.numLayers - 2, 0, -1):
			a = self.activations[el]
			gprime = a*(1.0 - a)
			d = numpy.dot(weightsTranspose[el], self.deltas[el + 1]) * a*(1.0 - a)
			self.deltas[el][:] = d[1:]

	def getOutput(self):
		"""
		Get the network output (excl. bias)
		@return array
		"""
		return self.activations[-1][1:]

	def getInput(self):
		"""
		Get the network input (excl. bias)
		@return array
		"""
		return self.activations[0][1:]

	def getCost(self, inputOutputList, lam=0.0):
		"""
		Compute cost function associated with input/output training data
		@param inputOutputList list of [(input, output), ...] values
		@param lam >= 0 regularization parameter (lam = 0 means no regularization)
		"""
		res = 0.0

		# standard term
		for x, y in inputOutputList:

			# output from inputs and weights
			out = self.forward(x)

			# error
			res -= numpy.sum( y*numpy.log(out) + (1.0-y)*numpy.log(1.0-out) )
		
		# regularization term 
		for w in self.weights:
			res += (lam/2.0) * numpy.sum(w[:, 1:]**2)

		res /= float(len(inputOutputList))

		return res

	def train(self, inputOutputList, lam=0.0, alpha=1.0):
		"""
		Update the weights using training set
		@param inputOutputList list of [(input, output), ...] values
		@param lam >= 0 regularization parameter (lam = 0 means no regularization)
		@param alpha > 0 gradient descent step
		@return cost before completion of step, cost after completion of step
		"""

		numTraining = len(inputOutputList)

		# accumulate the error
		for x, y in inputOutputList:

			# compute the activations at each level
			self.forward(x)

			# compute the errors at each level
			self.backward(y)

			for el in range(self.numLayers-1):
				# d J /d Theta
				self.bigDeltas[el] += numpy.outer(self.deltas[el+1], self.activations[el])

		cost = self.getCost(inputOutputList, lam)

		# update the weights across all layers
		for el in range(self.numLayers-1):
			self.weights[el][:, :] -= alpha*self.bigDeltas[el][:, :] / numTraining
			# regularization term
			self.weights[el][:, 1:] -= alpha*lam*self.weights[el][:, 1:]

		newCost = self.getCost(inputOutputList, lam)

		return cost, newCost
