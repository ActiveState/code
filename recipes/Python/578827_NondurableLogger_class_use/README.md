## NondurableLogger class for use with concurrent.futures.ProcessPoolExecutor's submit and map methods  
Originally published: 2014-02-08 15:52:07  
Last updated: 2014-02-10 17:50:59  
Author: Peter Santoro  
  
I needed a simple logging solution that I could use with with concurrent.futures.ProcessPoolExecutor and this is my initial recipe.