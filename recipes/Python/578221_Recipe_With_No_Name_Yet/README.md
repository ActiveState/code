## Recipe With No Name Yet  
Originally published: 2012-07-23 17:39:44  
Last updated: 2012-08-22 17:57:12  
Author: Cyril   
  
Not a very new recipe, but a short one and (I hope) useful :
  
  - wrapping any function "f" with two decorators "enter_event" and "exit_event" that will trigger calling of user
    functions when, ... hum ... evidently, **just before entering and just after exiting the "f" function**.

Typical usages :
  
  - debugging on a function by function basis :
    - emit a trace in log file to see when functions are called and check sequences correctness
      (very usefull when programming by events)
    - feed a profile analyzer (by fine tuning which functions are enabled)
    - feed a code coverage analyzer (  "  )
  - kind of validator on function calling :
    - implement programming by contracts :
      - check that parameters values of "f" function will not have an unexpected value or be of an unexpected type
      - this allow to increase code robustness by narrowing 
    - implement invariants (eg. check that returned value is always in the excepted range, ...)
    - insure that a function follow specifications by meta-checking that has always predictable results
	  (eg. return the fixed expected value for each possible input value, ...)
  - minimum modification of existing code
  - **in the same thinking line as the "monkey patching" concept**

Notes on usage :
   - recipe works on functions and any kind of methods (methods, class methods,
       and static methods)
   - the usage order of "@enter_event" and "@exit_event" decorators doesn't
       matter : the result will be the same

- *PLEASE VOTE FOR THIS RECIPE if you like it !*