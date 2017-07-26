######################################################################
## 
## Feature Broker
## 
######################################################################

class FeatureBroker:
   def __init__(self, allowReplace=False):
      self.providers = {}
      self.allowReplace = allowReplace
   def Provide(self, feature, provider, *args, **kwargs):
      if not self.allowReplace:
         assert not self.providers.has_key(feature), "Duplicate feature: %r" % feature
      if callable(provider):
         def call(): return provider(*args, **kwargs)
      else:
         def call(): return provider
      self.providers[feature] = call
   def __getitem__(self, feature):
      try:
         provider = self.providers[feature]
      except KeyError:
         raise KeyError, "Unknown feature named %r" % feature
      return provider()

features = FeatureBroker()

######################################################################
## 
## Representation of Required Features and Feature Assertions
## 
######################################################################

#
# Some basic assertions to test the suitability of injected features
#

def NoAssertion(obj): return True

def IsInstanceOf(*classes):
   def test(obj): return isinstance(obj, classes)
   return test

def HasAttributes(*attributes):
   def test(obj):
      for each in attributes:
         if not hasattr(obj, each): return False
      return True
   return test

def HasMethods(*methods):
   def test(obj):
      for each in methods:
         try:
            attr = getattr(obj, each)
         except AttributeError:
            return False
         if not callable(attr): return False
      return True
   return test

#
# An attribute descriptor to "declare" required features
#

class RequiredFeature(object):
   def __init__(self, feature, assertion=NoAssertion):
      self.feature = feature
      self.assertion = assertion
   def __get__(self, obj, T):
      return self.result # <-- will request the feature upon first call
   def __getattr__(self, name):
      assert name == 'result', "Unexpected attribute request other then 'result'"
      self.result = self.Request()
      return self.result
   def Request(self):
      obj = features[self.feature]
      assert self.assertion(obj), \
             "The value %r of %r does not match the specified criteria" \
             % (obj, self.feature)
      return obj

class Component(object):
   "Symbolic base class for components"

######################################################################
## 
## DEMO
## 
######################################################################

# ---------------------------------------------------------------------------------
# Some python module defines a Bar component and states the dependencies
# We will assume that
# - Console denotes an object with a method WriteLine(string)
# - AppTitle denotes a string that represents the current application name
# - CurrentUser denotes a string that represents the current user name
#

class Bar(Component):
   con   = RequiredFeature('Console', HasMethods('WriteLine'))
   title = RequiredFeature('AppTitle', IsInstanceOf(str))
   user  = RequiredFeature('CurrentUser', IsInstanceOf(str))
   def __init__(self):
      self.X = 0
   def PrintYourself(self):
      self.con.WriteLine('-- Bar instance --')
      self.con.WriteLine('Title: %s' % self.title)
      self.con.WriteLine('User: %s' % self.user)
      self.con.WriteLine('X: %d' % self.X)

# ---------------------------------------------------------------------------------
# Some other python module defines a basic Console component
#

class SimpleConsole(Component):
   def WriteLine(self, s):
      print s

# ---------------------------------------------------------------------------------
# Yet another python module defines a better Console component
#

class BetterConsole(Component):
   def __init__(self, prefix=''):
      self.prefix = prefix
   def WriteLine(self, s):
      lines = s.split('\n')
      for line in lines:
         if line:
            print self.prefix, line
         else:
            print

# ---------------------------------------------------------------------------------
# Some third python module knows how to discover the current user's name
#

def GetCurrentUser():
   return os.getenv('USERNAME') or 'Some User' # USERNAME is platform-specific

# ---------------------------------------------------------------------------------
# Finally, the main python script specifies the application name,
# decides which components/values to use for what feature,
# and creates an instance of Bar to work with
#
if __name__ == '__main__':
   print '\n*** IoC Demo ***'
   features.Provide('AppTitle', 'Inversion of Control ...\n\n... The Python Way')
   features.Provide('CurrentUser', GetCurrentUser)
   features.Provide('Console', BetterConsole, prefix='-->') # <-- transient lifestyle
   ##features.Provide('Console', BetterConsole(prefix='-->')) # <-- singleton lifestyle

   bar = Bar()
   bar.PrintYourself()

#
# Evidently, none of the used components needed to know about each other
# => Loose coupling goal achieved
# ---------------------------------------------------------------------------------
