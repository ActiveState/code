## Create module dependency graph   
Originally published: 2010-05-07 11:27:53  
Last updated: 2010-05-07 11:29:03  
Author: Noufal Ibrahim  
  
The following snippet will dump the module dependencies in a format that can be interpreted by the dot program distributed along with graphviz. You can use it like below to see the dependency graph for the asynchat module for example. (the program is saved as grapher.py)

    python grapher.py asynchat | dot -Tpng | display

A screenshot is available here http://twitpic.com/1lqnmh