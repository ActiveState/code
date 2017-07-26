## Monte Carlo Engine : How to find the optimised wager for next bet, following a recent loss.  
Originally published: 2014-04-28 08:40:35  
Last updated: 2014-04-28 08:41:49  
Author: alexander baker  
  
Simple Engine to help understand how to best wager your next bet, given that you just made a loss. The engine uses the modified Powell method to optimise the weight to apply to your wager on the next position.

{'My Simple Heads And Tails Model': <BackTest.Simulation object at 0x0583D410>}
participants [100] survivors [90.0%] losers [10.0%] weight [0.073858]
solving for r:  [ 0.07385806]
simulations 100, trials 100 starting pot 1000
calling initialise
{'My Simple Heads And Tails Model': <BackTest.Simulation object at 0x0583D430>}
participants [100] survivors [86.0%] losers [14.0%] weight [0.072220]
solving for r:  [ 0.07221954]
Optimization terminated successfully.
         Current function value: 8.000000
         Iterations: 2
         Function evaluations: 30
highest survivability following loss, multiply wager by 7.2949 %
.
----------------------------------------------------------------------
Ran 2 tests in 25.545s

OK