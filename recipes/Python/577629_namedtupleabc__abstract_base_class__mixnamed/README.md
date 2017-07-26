## namedtuple.abc - abstract base class + mix-in for named tuples  
Originally published: 2011-03-31 21:55:43  
Last updated: 2011-04-02 02:07:00  
Author: Jan Kaliszewski  
  
If you need

* to define **named tuple subclasses** (including reusable abstract ones), adding/overriding some methods, in a convenient way;
* to have the named tuple ABC (abstract base class) for **isinstance/issubclass** tests;
* or simply would like to define your named tuple classes in a **class-syntax-based and DRY way** (without repeating type names...)

-- **this recipe is for you.**