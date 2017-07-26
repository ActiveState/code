## Automatic fields pickling  
Originally published: 2005-11-18 14:35:50  
Last updated: 2005-11-20 23:28:34  
Author: Ori Peleg  
  
A 'fields' class is a class that acts like a struct full of fields, e.g.:

<pre>
class Titles:
  def __init__(self, name): self.name = name
  def dr(self): return "Dr. " + self.name
  def mr(self): return "Mr. " + self.name
</pre>

Once an instance is constructed, the return value of x.dr() or x.mr() doesn't change.

I sometimes have 'fields' classes that I need to pickle (e.g. they go over a wire) but they contain unpickleable members, like file objects or tracebacks.

This code adds picklers to such classes that automatically 'flattens' the instances on pickling, saving the return values and making the unpickled instance return the saved values.