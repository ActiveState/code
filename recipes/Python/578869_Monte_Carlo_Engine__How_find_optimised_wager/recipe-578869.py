'''
    monte carlo tool for simple strategy, more generally for use with any
    strategy that I want to back test...

    Engine takes a class instance, derived from a base class wih two methods
    
    initialise()
    onsimulation()
    aftersimulation()
    ontrial()
    finalise()


'''

import unittest, datetime
import numpy as np
from BackTest import MonteCarloModel, MonteCarloEngine, Simulation 
import matplotlib.pyplot as plt
from random import randint 
from scipy.optimize import fmin_powell
from hashlib import md5
from time import localtime

def Root2(r,verbose=True):
    '''
        simple wrapper routine for solver. returns the energy level for a given R=r.
        the solver can use this method to minimise the energy by varying r as necessary.
    '''
    if r <= 0:
        return 1e99
    else:
        e = MonteCarloEngine(moduleName='MonteCarloHeadsTailsExample', className='SimpleHeadTailModel')
        losers = e.start(args={'wager_multiplier':r})
        if verbose: print 'solving for r: ', r
        return losers              
        

class SimpleHeadTailModel(MonteCarloModel):
    '''
      model wager
      previous bet success or not, impact to profit.
        
    '''
    
    def toss(self):
        '''
            1 - win
            -1 - loss
            Each toss determines whether the position is successful or not. This way no need to keep track of a decision
            and an associated variable. Simply do I win or not.
        '''
        coin_toss = randint(1,2)
        if coin_toss == 1:
            return 1
        else:
            return -1
            
    def initialise(self, context):
                
        self.name = 'My Simple Heads And Tails Model'
        # start with 10 USD bet
        self.wager= 100
        self.wager_initial= 100
        self.starting_pot = 1000
        
        self.previous_value = 1 # default to 1 on first round
        self.simulations = 100    # MC simulation trials        
        self.trials = 100   # subintervals

        self.r = np.zeros(shape=(self.simulations, self.trials), dtype=float) # matrix to hold all results
        self.pnl = np.zeros(shape=(self.simulations, self.trials), dtype=float) # matrix to hold all results
        print "simulations %d, trials %d starting pot %d " % (self.simulations, self.trials, self.starting_pot)
        
        # Tell the engine where to associate the data to security.        
        context[self.name] = Simulation(self.simulations, self.trials, self.toss)
    
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(211)
        self.ax1 = self.fig.add_subplot(212)
        self.ax.autoscale_view(True,True,True)        
                        
    
    def onsimulation(self, model, simulation, engine):        
        self.r[simulation,0] = 0
        # assume starting pot here
        self.pnl[simulation,0] = self.starting_pot
        
    def aftersimulation(self, model, simulation, engine):
        self.ax.plot(np.arange(0, self.trials, 1), self.r[simulation])        
        self.ax1.plot(np.arange(0, self.trials, 1), self.pnl[simulation])
        
    def reset_wager(self):
        self.wager = self.wager_initial
        
    def ontrial(self, model, simulation, trial, value, engine, args):
        '''
            want to test some strategies for betting
            set wager for each bet
            if previous bet

            value : float
                sample from model
            
        '''
                     
	   
        # if we lost last time then double up		
		
        if self.previous_value == -1:
		if args.has_key('args'):
                	self.wager = (self.wager*float(args['args']['wager_multiplier'][0]))
		else:
			self.wager = (self.wager*0.1)      
        
        # keep track of coin toss paths
        self.r[simulation,trial] = self.r[simulation,trial-1] + value
        if args.has_key('args'):
            self.r0 = float(args['args']['wager_multiplier'][0])
        else:
			self.r0 =0.1
        # if we won, add the wager
        # else subtract the wager
        
        if self.pnl[simulation,trial-1] > 0:        
            if value == 1 :
                self.pnl[simulation,trial] = self.pnl[simulation,trial-1] + self.wager
            else:
                self.pnl[simulation,trial] = self.pnl[simulation,trial-1] - self.wager
        else:
            # no bet to be made here
            self.pnl[simulation,trial] = self.pnl[simulation,trial-1]
             
        # always reset wager    
        self.reset_wager()
        
        # keep track of the previous value for next time around
        self.previous_value = value
        
	def add_prefix(self, filename):
		from hashlib import md5
		from time import localtime
		return "%s_%s"%(md5(str(localtime())).hexdigest(), filename)	
		
    def finalise(self, model, engine):  
		'''
			returns the value that we are trying to minimise, here the number of losers.
		'''
        
	# what is our survivability

		number_of_losers = len([f for f in self.pnl if f[len(f)-1]<=0])
		number_of_survivors = len([f for f in self.pnl if f[len(f)-1]>0])
		number_of_participants = len(self.pnl)
		print "participants [%d] survivors [%2.1f%%] losers [%2.1f%%] weight [%2.6f] "% (number_of_participants, float(number_of_survivors)/float(number_of_participants)*100, float(number_of_losers)/float(number_of_participants)*100, self.r0)

		plt.title('Simulations %d Steps %d' % (int(self.simulations), int(self.trials)))
		plt.xlabel('steps')
		plt.ylabel('profit and loss')					
		plt.savefig("%s_%s"%(md5(str(localtime())).hexdigest(), 'model'))
		return float(number_of_losers)/float(number_of_participants)*100
        
		
class TestNode(unittest.TestCase):
    def setUp(self):
        pass    
   
    def test_engine(self):
        '''
            example of how to launch the MontoCarloTestEngine
            this is modelled on the quantopian style interface.
        '''		
        e = MonteCarloEngine(moduleName='MonteCarloHeadsTailsExample', className='SimpleHeadTailModel')
        e.start()
    
    def test_minimise(self):
                
        print '#################################'
        print '# Test Equilibrium Loss Wager'
        print '#################################'
        
        wager_multiplier=fmin_powell(Root2, x0=1., maxiter=20)
        print "highest survivability following loss, multiply wager by %2.4f %% "%(wager_multiplier*100)

if __name__ == '__main__':
    unittest.main()


==================================================================
== BackTest module
==================================================================


'''
	back testing tool for prediction strategy, more generally for use with any
	strategy that I want to back test...

	Engine takes a class instance, derived from a base class wih twomethods

	
	initialise()
	ondata()


'''

import unittest, time, datetime
from pandas import DataFrame
import numpy as np
from pylab import show
import random
from abc import ABCMeta, abstractmethod
import pandas as pd

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
	def ontrial(self, model, simulation, trial, value, engine, args):
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
			#print isinstance(self.obj, MonteCarloModel), hasattr(self.obj, 'initialise')
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
			#print instance 
			return instance

		def start(self, **args):
			#print 'starting...', self.obj, self.context, args		
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
								self.obj.ontrial(model, simulation, trial, value, self, args)
																
						# call to signal after simulation
						if hasattr(self.obj, 'aftersimulation'):
							self.obj.aftersimulation(model, simulation, self)					
					#self.post_ondata(k, index2, value)
							
			if hasattr(self.obj, 'finalise'):
				return self.obj.finalise(model, self)
	
'''
class ExampleModel(BackTestModel):

	def initialise(self, context):
		context['ARM.L'] = 'Book1.csv'
		print 'setting ARM.L' 
		
	def ondata(self, sid, data):
		print sid, data
'''
class Engine(Component):
	'''
		responsible for handling instances of the back test models
	'''
	def __init__(self, moduleName, className):
		
		self.context = {}
		self.data = {}
		self.orders = {}
		self.positions = {}
		self.pnl = {}
		self.risk = {}

		self.obj = self.__generate__(moduleName, className)
		#print isinstance(self.obj, BackTestModel), hasattr(self.obj, 'initialise')
		if isinstance(self.obj, BackTestModel):
			if hasattr(self.obj, 'initialise'):
				self.obj.initialise(self.context)
				#print 'calling initialise'
			else:
				print 'no initialise'
		#
		# TODO: load data from somewhere for securities in context
		#	
		#print self.context	
		for k in self.context.keys():
			#print k
			t = time.clock()
			myfilename = self.context[k]
		      	data = DataFrame.from_csv(myfilename,header=0,index_col=0,parse_dates=True)	
			print 'load data', time.clock()-t						
			self.data[k] = data
			self.positions[k] = 0
			self.pnl[k] = 0
			self.risk[k] = 0
	
	def order(self, sid, value):
		# queue order to be processed
		self.orders[sid] = (value, False)
	
	@property
	def position(self):
		return self.positions
	
	def __generate__(self, module_name, class_name):
		module = __import__(module_name)
		class_ = getattr(module, class_name)
		instance = class_()
		print instance 
		return instance
	
	def post_ondata(self, sid, index, value):
		# process orders
		for k in self.context.keys():
			if hasattr(self, 'orders'):
				if len(self.orders) == 0:
					print 'no orders'
					break			
				
			m_size, m_processed = self.orders[k]
			# check we have not processed this order already.
			if not m_processed:
				if not (self.positions[k]+ m_size <= 0):				
					self.positions[k] += m_size
					print 'ordering %d of %s, total %d' % (m_size, k, self.positions[k])
					self.orders[k] = None
				else:
					print 'no short selling'				
		# handle pnl and risk
		# tick() charts
		

	def start(self):
		print 'starting...', self.obj, self.context		
		if not self.obj is None:	
			for k in self.context:
				for i, (index, value) in enumerate(self.data[k]['value'].iteritems()):					
					index2 = datetime.datetime(pd.to_datetime(index).year
											, pd.to_datetime(index).month
											, pd.to_datetime(index).day)					
					self.obj.ondata(k
								, index2
								, value
								, self.data[k]['value'][0:i]
								, self)					
					self.post_ondata(k, index2, value)					
