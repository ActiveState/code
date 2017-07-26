# You can insert the folowing two lines 
# to your program to make NullClass available.

class NullClass:
   def __getattr__(self,name): return lambda *x,**y: None

# -------------------------------------------
# Example: switched writing to a logfile

log=err=NullClass()
if verbose:
   log = open('/tmp/log')
   err = open('/tmp/err')

log.write('blabla')
err.write('blabla error')

#This obviously avoids the usual pollution from stuff like "if verbose: ".
#NullClass also accepts keyword arguments.  
