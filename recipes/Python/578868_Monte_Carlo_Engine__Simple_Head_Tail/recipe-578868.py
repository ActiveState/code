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
from engine.BackTest import MonteCarloModel, MonteCarloEngine, Simulation 
import matplotlib.pyplot as plt
from random import randint 

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
        self.simulations = 10    # MC simulation trials        
        self.trials = 100   # subintervals        
        self.r = np.zeros(shape=(self.simulations, self.trials), dtype=float) # matrix to hold all results
        self.pnl = np.zeros(shape=(self.simulations, self.trials), dtype=float) # matrix to hold all results
        
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
        
    def ontrial(self, model, simulation, trial, value, engine):
        '''
            want to test some strategies for betting
            set wager for each bet
            if previous bet

            value : float
                sample from model
            
        '''
                        
        # if we lost last time then double up
        if self.previous_value == -1:
            self.wager += self.wager      
        
        # keep track of coin toss paths
        self.r[simulation,trial] = self.r[simulation,trial-1] + value
        
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
        
    def finalise(self, model, engine):                    
        plt.title('Simulations %d Steps %d' % (int(self.simulations), int(self.trials)))
        plt.xlabel('steps')
        plt.ylabel('profit and loss')
        plt.show()
        
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
        

if __name__ == '__main__':
    unittest.main()
