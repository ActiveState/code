import unittest, datetime
import numpy as np
from engine.BackTest import MonteCarloModel, MonteCarloEngine, Simulation 
import matplotlib.pyplot as plt
from matplotlib.dates import date2num, DateFormatter, DayLocator
from pandas import DataFrame

from numpy.random import standard_normal
from numpy import array, zeros, sqrt, shape

class SimpleMonteCarloModel(MonteCarloModel):
    '''
        simple example implementation of a model. This will be back tested based on the data
        passed to the initialise method.
        
        class ExampleModel(MonteCarloModel):

                def initialise(self, context):
                    context['My Simple Model'] = Simulation(10, 100, standard_normal()) 
                    print 'setting My Simple Model' 
                    
                def ondata(self, model, simulation, trial, value, engine):
                    print simulation, trial, value, engine
        
    '''
    def initialise(self, context):
        
        self.r0 = 0.05 # current UK funding rate
        self.theta = 0.10 # 1 % long term interest rate
        self.k = 0.3
        self.beta = 0.03
         
        ## simulate short rate paths
        self.n = 1000    # MC simulation trials
        self.T = 24.    # total time
        self.m = 100   # subintervals
        self.dt = self.T/self.m  # difference in time each subinterval
        self.r = np.zeros(shape=(self.n, self.m), dtype=float) # matrix to hold short rate paths
        
        # Tell the engine where to associate the data to security.        
        context['My Simple Model'] = Simulation(self.n, self.m, standard_normal)
    
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)
        self.ax.autoscale_view(True,True,True)        
                        
    
    def onsimulation(self, model, simulation, engine):
        #print 'new simulation,', model, simulation
        #plot(np.arange(0, T, dt), r[j])
        self.r[simulation,0] = self.r0
        
    def aftersimulation(self, model, simulation, engine):
        self.ax.plot(np.arange(0, self.T, self.dt), self.r[simulation])        
        
    def finalise(self, model, engine):
        
        self.t = np.arange(0, self.T, self.dt)
        self.rT_expected = self.theta + (self.r0-self.theta)*pow(np.e,-self.k*self.t)
        self.rT_stdev = sqrt( pow(self.beta,2)/(2*self.k)*(1-pow(np.e,-2*self.k*self.t)))
        #print 'expected', self.rT_expected, 'std', self.rT_stdev
        
        self.ax.plot(self.t, self.rT_expected, '-+r')
        self.ax.plot(self.t, self.rT_expected+2*self.rT_stdev, '-b')
        self.ax.plot(self.t, self.rT_expected-2*self.rT_stdev, '-b')
        self.ax.plot(self.t, self.rT_expected+4*self.rT_stdev, '-g')
        self.ax.plot(self.t, self.rT_expected-4*self.rT_stdev, '-g')
        
        print shape(self.t), shape(self.r)
        
        plt.title('Simulations %d Steps %d r0 %.2f alpha %.2f beta %.2f sigma %.2f' % (int(self.n), int(self.m), self.r0, self.k, self.theta, self.beta))
        plt.xlabel('steps')
        plt.ylabel('short term interest rate')
        plt.show()
        
    def ontrial(self, model, simulation, trial, value, engine):
        '''
            called when we have some new data to play into the model.
            each call is an event

            value : float

                sample from model
            
        '''
        #print simulation, trial, value
        # evaluation the model step.
        self.r[simulation,trial] = self.r[simulation,trial-1] + self.k*(self.theta-self.r[simulation,trial-1])*self.dt + self.beta*sqrt(self.dt)*value;
        
        
class TestNode(unittest.TestCase):
    def setUp(self):
        pass    
   
    def test_engine(self):
        '''
            example of how to launch the BackTestEngine
            this is modelled on the quantopian style interface.
        '''
        e = MonteCarloEngine(moduleName='MonteCarloTestExample', className='SimpleMonteCarloModel')
        e.start()
        

if __name__ == '__main__':
    unittest.main()



import unittest, time, datetime
from abc import ABCMeta, abstractmethod

#
# Simple python component wrapper
#

class Component(object):
	__metaclass__ = ABCMeta
	
	@abstractmethod
	def start(self):
		raise NotImplementedError("Should implement intialise()!")
		

class BackTestModel(object):
	__metaclass__ = ABCMeta
	
	@abstractmethod
	def initialise(self, context):
		raise NotImplementedError("Should implement intialise()!")
	
	@abstractmethod	
	def ondata(self, sid, data):
		raise NotImplementedError("Should implement ondata()!")			
	
class MonteCarloModel(object):
	__metaclass__ = ABCMeta
	
	@abstractmethod
	def initialise(self, context):
		raise NotImplementedError("Should implement intialise()!")
	
	@abstractmethod	
	def ontrial(self, model, simulation, trial, value, engine):
		raise NotImplementedError("Should implement ontrial()!")
	
	def onsimulation(self, model, simulation, engine):
		raise NotImplementedError("Should implement onsimulation()!")
	
	def aftersimulation(self, model, simulation, engine):
		raise NotImplementedError("Should implement aftersimulation()!")
	
	def finalise(self, model, engine):
		raise NotImplementedError("Should implement finalise()!")
	
	
class Simulation(object):
	'''
		simple wrapper that describes a simulation
	'''
	
	def __init__(self, n, m, func):
		'''
			n integer
				number of simulations
			m integer
				number of trials per simulation
			func class method or function
				used to sample the value
		'''
		self.number_of_simulations = n
		self.number_of_trials = m
		self.func = func	
		
	@property
	def sample(self):
		return self.func
	
class MonteCarloEngineException(Exception):
	pass	
	
class MonteCarloEngine(Component):
		'''
			twist on the Engine that will take a different type of context, this time
			a Simulation class instance. This will be called
			
			
			class ExampleModel(MonteCarloModel):

				def initialise(self, context):
					context['My Simple Model'] = Simulation(10, 100, standard_normal()) 
					print 'setting My Simple Model' 
					
				def ondata(self, model, simulation, trial, value, engine):
					print simulation, trial, value, engine
			 
		'''
		def __init__(self, moduleName, className):
			self.context = {}			
			self.obj = self.__generate__(moduleName, className)
			print isinstance(self.obj, MonteCarloModel), hasattr(self.obj, 'initialise')
			if isinstance(self.obj, MonteCarloModel):
				if hasattr(self.obj, 'initialise'):
					self.obj.initialise(self.context)
					print 'calling initialise'
				else:
					print 'no initialise'
			#
			# TODO: load data from somewhere for securities in context
			#	
			print self.context	
		
		def __generate__(self, module_name, class_name):
			module = __import__(module_name)
			class_ = getattr(module, class_name)
			instance = class_()
			print instance 
			return instance

		def start(self):
			print 'starting...', self.obj, self.context		
			if self.obj is None:
				raise MonteCarloEngineException('No engine exists')
		 	
			for name, model in self.context.items():										
				for simulation in np.arange(0, model.number_of_simulations): # number of MC simulations
						# call to signal new simulation
						if hasattr(self.obj, 'onsimulation'):
							self.obj.onsimulation(model, simulation, self)
							
						for trial in np.arange(1,model.number_of_trials): #trials per simulation						
							value = model.sample()				
							if hasattr(self.obj, 'ontrial'):								
								self.obj.ontrial(model, simulation, trial, value, self)
																
						# call to signal after simulation
						if hasattr(self.obj, 'aftersimulation'):
							self.obj.aftersimulation(model, simulation, self)					
					#self.post_ondata(k, index2, value)
							
			if hasattr(self.obj, 'finalise'):
				self.obj.finalise(model, self)
