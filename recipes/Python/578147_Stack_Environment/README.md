## Stack Environment  
Originally published: 2012-05-29 14:47:23  
Last updated: 2017-06-22 10:24:05  
Author: Alfe   
  
The environment variables of processes get inherited by their children who can modify them and pass them on to their children.  The tree of processes is similar to the call tree of a running Python process, but a similar mechanism like the environment variables is missing.  I'm offering a solution for this; each stack frame takes the place of a process, hence I call it StackEnv.  It comes in handy if you want to pass information from one frame to a frame far below without patching all the calls in between to pass the data (which might belong to a framework you don't want to change).

Usecases:

1. You call a framework which calls back your code before returning (e. g. in passed objects you provide).  You want to pass some information to your code without relying on global variables or similar constructs which weren't thread-safe nor re-entrant.

2. You want to pass pseudo-global but in fact situation-related information (e. g. the verbosity based on the situation the call comes from) without handing the information down in each and every call which can happen below yours.

3. You want to give called methods the option to override the decision of the caller method regarding this information.  (E. g. the caller decides that verbosity should be True, but the called method then calls another method and decides that the verbosity in this case should be False.)

Alike processes, called frames cannot influence the values for calling frames (but of course mutable values *can* be used to pass information upwards; this normal kind of "abuse" isn't prevented).

Importing:

    from stackEnv import stackEnv

Setting a stackEnv variable:

    stackEnv.verbose = True

Using the value of a stackEnv variable:

    if stackEnv.verbose: print "being verbose now"

Testing a stackEnv variable:

    if 'verbose' in stackEnv: print "having information on verbosity"

Overriding a stackEnv variable's value for the rest of this frame and its calls:

    stackEnv.verbose = False

Removing a stackEnv variable for the rest of this frame and its calls:

    del stackEnv.verbose

Some more useful API of this class can be found in the unit test included.