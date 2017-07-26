##from __future__ import generators # for Python 2.2

######################################################################
## 
## public interface
## 
######################################################################

# SetElemCombinations.py

def ByNestedComprehnsionAlogrithm(*sets):
   """Returns a list of all element combinations from the given sets.
      A combination is represented as a tuple, with the first tuple
      element coming from the first set, the second tuple element
      coming from the second set and so on.
      A set may be any iterable to which the not operator is applicable.
   """
   g = []
   for set in sets:
      if not set: return []
      if g:
         g = [ i + (j,) for i in g for j in set ]
      else:
         g = [(j,) for j in set]
   return g

def ByRecursiveGeneratorAlrgorithm(*sets):
   """Returns a generator that yields one tuple per element combination.
      A set may be any iterable to which the not operator is applicable.
   """
   if not sets: return
   def calc(sets):
      head, tail = sets[0], sets[1:]
      if not tail:
         for e in head:
            yield (e,)
      else:
         for e in head:
            for t in calc(tail):
               yield (e,) + t
   return calc(sets)

def ByDynamicallyGeneratedCode(*sets):
   if not sets: return []
   F = MakeListComprehensionFunction ('F', len(sets))
   return F(*sets)

def MakeListComprehensionFunction (name, nsets):
   """Returns a function applicable to exactly <nsets> sets.
      The returned function has the signature
         F(set0, set1, ..., set<nsets>)
      and returns a list of all element combinations as tuples.
      A set may be any iterable object.
   """
   if nsets <= 0:
      source = 'def %s(): return []\n' % name
   else:
      constructs = [ ('set%d'%i, 'e%d'%i, 'for e%d in set%d'%(i,i))
                     for i in range(nsets) ]
      a, e, f = map(None, *constructs)
      ##e.reverse() # <- reverse ordering of tuple elements if needed
      source = 'def %s%s:\n   return [%s %s]\n' % \
               (name, _tuplestr(a), _tuplestr(e), ' '.join(f))
   scope = {}
   exec source in scope
   return scope[name]

def _tuplestr(t):
   if not t: return '()'
   return '(' + ','.join(t) + ',)'


######################################################################
## 
## demo
## 
######################################################################

ListOfCombinations = ByDynamicallyGeneratedCode
GenerateCombinations = ByRecursiveGeneratorAlrgorithm

if __name__ == '__main__':
   print

   print 'All possible 3-bit binary numbers:'
   all = ListOfCombinations(*[(0,1)]*3)
   print '\t', ', '.join([ ''.join(map(str, digits)) for digits in all ])
   numbers = [ reduce(lambda n, d: n << 1 | d, digits, 0)
               for digits in all ]
   print '\t', ', '.join(map(str, numbers))

   print 'Some controverse statements:'
   all = ListOfCombinations( ('python', 'ruby'),
                             ('is cool', 'is ok', 'sucks') )
   for each in all:
      print '\t', ' '.join(each).capitalize()

   # When you need several combinations from N (possibly different) sets
   # increase speed by obtaining a function for N sets ...
   print 'Several combinations from 2 sets:'
   F = MakeListComprehensionFunction('F', 2)
   print '\t', F( (1,2,3), (10,20) )
   print '\t', F( '+-', 'x' )

   # When you need to iterate through lots of combinations,
   # save memory using a generator ...
   print 'Some binary operations:'
   G = GenerateCombinations( 'ab', '+-*/', 'x' )
   for each in G:
      print '\t', ' '.join(each)
   print 'Some binary operations calculated by ByNestedComprehnsionAlogrithm:'
   G = ByNestedComprehnsionAlogrithm( 'ab', '+-*/', 'x' )
   for each in G:
      print '\t', ' '.join(each)
