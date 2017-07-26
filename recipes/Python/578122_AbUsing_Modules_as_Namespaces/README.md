## (Ab)Using Modules as Namespaces  
Originally published: 2012-05-10 03:58:33  
Last updated: 2012-05-10 04:14:06  
Author: Wolfgang Scherer  
  
I have previously built a shar-like Python utility, which reads (marked) imported modules, gzips and base64 encodes them, then generates a python script, which is fully standalone.

The included module source is placed into sys.modules at runtime, making imports possible without actually having the module files installed. A very nice thing for administrative scripts that have to work in unconfigured environments.

At that time I discovered a lot of information about how modules in Python work.

Reading the very interesting recipe at http://code.activestate.com/recipes/577887-a-simple-namespace-class/
made me realize, that modules are actually very useful as generic namespaces too.
