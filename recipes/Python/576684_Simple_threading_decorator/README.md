###Simple threading decorator

Originally published: 2009-03-08 15:46:56
Last updated: 2009-03-10 01:38:51
Author: david.gaarenstroom 

When you're new at threading, using threads can be a bit daunting at first. If all you want is just to "run this function in parallel (= asynchronously) to the main program code", then this recipe can be of use. Simply use "@run_async" as a decorator for the function you want to run asynchronously. A call to that function will return immediately but the function itself will run in parallel.