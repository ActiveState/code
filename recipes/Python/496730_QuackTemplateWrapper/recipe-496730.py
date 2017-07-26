"""
A quick-and-dirty template helper, using Python's "duck"-typing approach.

Usage: Wrap an object in QuackTemplate.Wrapper, and use it with a normal
       Python template, like so:
      
       print "%(attribute)s" % Wrapper(myObj)

       See __main__ below for test cases and examples.

       NB: QuackTemplate can follow encapsulated objects, lists and dicts,
           but it can only call methods WITH ZERO arguments.

Costas Malamas 2006.02.22
"""
import types

class Wrapper:
   def __init__(self, obj):
      self.obj = obj

   def __repr__(self):
      return str(self.obj)

   def __getitem__(self, key):
      #
      # Null key, same as repr of self
      #
      if not key:
         return str(self)
      #
      # If there is a dereference, split the call
      #
      rem = None
      idx = None
      if "." in key:
         key, rem = key.split('.', 1) 
      if '#' in key:
         key, idx = key.split('#', 1)
      try:
         result = getattr(self.obj, key)
      except AttributeError:
         #
         # Allow for last-minute additions to wrappers; if a key doesn't 
         # exist in the wrapped object, first test ourselves, then delegate
         #
         if self.__dict__.get(key):
            result = self.__dict__[key]
         else:
            try:
               result = self.obj[key]
            except:
               raise Exception, "Key '%s' (remainder: '%s') not found in object of type %s!" %\
                  (key, rem, self.obj.__class__)
      except Exception, mesg:
         print "Wrapper %s with key %s and remainder %s" % (str(self), key, rem)
         print mesg
         raise Exception

      #
      # If calling a member instance, delegate to it!
      #
      if type(result) == types.InstanceType:
         return Wrapper(result)[rem]
      #
      # A method could return either another object
      # or a result, so delegate the interim result
      #
      elif type(result) == types.MethodType:
         interim = result()
         return Wrapper(interim)[rem]
      elif idx and type(result) == types.ListType:
         return Wrapper(result[int(idx)])[rem]
      elif rem:
         return Wrapper(result[rem])
      return Wrapper(result)[rem]

if __name__ == "__main__":
   class Test:
      def __init__(self):
         self.var    = "a String!"
         self.intvar = 20
         self.data = [1, 2]
         self.lut = {"key" : 999}

      def get(self):
         return "from get()!"

      def factory(self):
         return Test()

      def __repr__(self):
         return "A Test instance!"

   z = Test()
   z.child = Test()
   z.child.child = Test()
   z.child.children = [Test(), Test()]
   wz = Wrapper(z)
   zz = Wrapper(Test())
   wz.whatever = Wrapper(zz)

   print "String attribute: %(var)s" % wz
   print "Integer attribute: %(intvar)s" % wz
   print "Method call: %(get)s" % wz
   print "Attribute of a child: %(child.var)s" % wz
   print "Method of a grand-child: %(child.child.get)s" % wz
   print "Method of a generated object: %(child.factory.get)s" % wz
   print "Repr of a generated object: %(child.child)s" % wz
   print "Item of an encaps'ed list object: %(child.data#1)s" % wz
   print "Value of a generated object's dict: %(child.lut.key)s" % wz
   print "Method of an encaps'ed obj in a list: %(child.children#1.get)s" % wz
   print "Dynamic addition to a wrapper: %(whatever.get)s" % wz

   x = {"one": Wrapper(Test()), "two" : 4}
   wx = Wrapper(x)
   print "Object method in a dict: %(one.get)s" % wx
   print "Value in a dict: %(two)s" % wx
