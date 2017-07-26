## Clear Only Project Modules  
Originally published: 2014-12-17 19:03:14  
Last updated: 2014-12-17 19:03:15  
Author: Cornelius Jatniel Prinsloo  
  
Useful for python sessions that have a long startup time
because of external dependancies
[In my case that would be pygame and pymunk]
I've got a slow computer so it takes a while to startup
this is the solution I came up with

import this before any other of your project imports
example:
    import reloading # The modules in your project folder get cleared
then load the rest of your project modules

make sure that the reloading script is in your project folder, or else it won't work

You might be able to extend this by changing line