###Just in time instantiation

Originally published: 2003-12-10 19:28:45
Last updated: 2003-12-10 19:28:45
Author: Justin Shaw

I frequently find myself adding "just in time" (JIT) object creation to avoid wasting cycles on objects that are never used.  This class enables JIT object creation by basically currying the __init__ method.\n\nThe object is instianted only when an attribute is got or set.  Then automatic delegation is used to front for the object (see http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/52295)