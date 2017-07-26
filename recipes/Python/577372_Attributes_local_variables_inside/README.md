## Attributes as local variables inside a with clause 
Originally published: 2010-08-25 16:39:25 
Last updated: 2010-08-25 16:42:13 
Author: Joakim Pettersson 
 
This recipe defines three context managers that make it easier to step in and out of different parameter sets (‘Attributes’), allows data inheritance on such data sets (‘Scope’) and lets remote interpreters behave likewise (‘Workspace’). Just use “with object:” and there you have all its attributes ready to use as local variables. Changes are committed back into the object on exit from the ‘with’ clause. 