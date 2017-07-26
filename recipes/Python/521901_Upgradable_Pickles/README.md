## Upgradable Pickles  
Originally published: 2007-06-12 19:34:08  
Last updated: 2007-06-16 16:17:06  
Author: Justin Shaw  
  
Stale Pickles ... New Classes.  Pickles are by far the easiest way to achieve persistent objects in Python.  A problem arises however, when a class is modified between the time when an object is pickled and when it is un-pickled.  When a stale pickle is extracted, the old data is coupled with the new class code.  This is not a problem as long as no new data attributes are required.  For instance, a new method that relies only on old data may be added and still work with the old pickle.\n\nOf course, if attributes are added, the old pickle files will no longer function correctly with the new class definition.\n\nThis recipe provides a framework for writing upgradable classes that support backward compatibility with stale pickles.