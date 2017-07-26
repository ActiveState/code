## Releasing a Resource used by a Generator  
Originally published: 2002-05-31 05:00:15  
Last updated: 2002-05-31 05:00:15  
Author: Michael Chermside  
  
Since try-finally can't be used in a generator, it can be somewhat tricky to ensure that a resource is released if the generator is exited early. This solution wraps the generator with an enclosing class to ensure the resource is released.