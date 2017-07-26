# -- use cases: --

def usecases():
   from pprint import pprint

   print '\n--- Sorting Simple Lists ---\n'
   data = ['Jim', 'Will', 'Tom']
   print data
   data.sort( By(len) )
   print data

   print '\n--- Sorting Simple Tables ---\n'
   data = [
      ('Jim', 21),
      ('Will', 24),
      ('Tom', 20),
      ]
   pprint(data)
   data.sort( ByColumn(0) ) # using straight forward comparator closure
   pprint(data)
   data.sort( By(Column(1)) ) # comparator/accessor closure combination
   pprint(data)

   print '\n--- Sorting Object Tables ---\n'
   class Record:
      def __init__(self, **kw): self.__dict__.update(kw)
      def __repr__(self): return '<record %r>' % self.__dict__
   data = [
      Record(name='Jim', age=21),
      Record(name='Will', age=24),
      Record(name='Tom', age=20),
      ]
   pprint(data)
   data.sort( ByAttribute('name') ) # using straight forward comparator closure
   pprint(data)
   data.sort( By(Attribute('age')) ) # comparator/accessor closure combination
   pprint(data)


# -- a straight forward approach: --

def ByColumn(key):
   def compare(obj1, obj2): return cmp(obj1[key], obj2[key])
   return compare

def ByAttribute(name):
   def compare(obj1, obj2): return cmp(getattr(obj1, name), getattr(obj2, name))
   return compare

# -- a somewhat more generic approach: --

def By(accessor):
   def compare(left, right): return cmp( accessor(left), accessor(right) )
   return compare
def Attribute(name):
   def get(obj): return getattr(obj, name)
   return get
def Column(key):
   def get(obj): return obj[key]
   return get

# -- demo: --

if __name__ == '__main__':
   usecases()
