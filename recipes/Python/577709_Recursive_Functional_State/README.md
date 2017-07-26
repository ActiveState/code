## Recursive Functional State Machine  
Originally published: 2011-05-20 13:46:48  
Last updated: 2011-05-20 13:46:48  
Author: Stefan Tunsch  
  
This is a simple state machine that takes a functional approach.
It requires trampoline from pysistence.func to avoid the recursion limit.

Namedtuples are used to define the different states.
globals() is used to reference the states. (This could also be done putting states into a separate module and getting them through getattr.)

In this recipe the functions called in the different states need to return a boolean, which defines the success or failure event.