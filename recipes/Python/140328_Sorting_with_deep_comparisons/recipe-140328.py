class DeepSort(object):  # Python 2.2.x version
   """
   Sorts a list of objects  by either attribute or index  across a prioritized
   group of attributes, indices, or both.

   Usage:
      dSort = DeepSort()
      dSort(Alist [, val1] [..., valN])

   Where val may be an integer, a string, a tuple or list. When val is an int-
   eger,  it represents  the index of a  value in an object.  When  val  is  a
   string,  it represents an  attribute of an object. When val is a tuple or a
   list, it may contain only integers (indices) or strings  (attributes).   If
   needed, vals may be passed as a single tuple or list:
      dSort(Alist [, (val1, [..., valN])])

   Objects may be compared to an  arbitrary depth of  indices/attributes (e.g.
   sort(Alist,(0, 'a'),(1, 'a')) will sort each object according to its second
   level of attr / index (by obj[0]['a'] first, then by obj[1]['a'] needed)).
   """
   # If all comparisons but 1 fail with exceptions, a sort will still occur.

   def __init__(self):
      
      self.vals = None
      self.valTypes = (type(1), type('a'))
      self.seqTypes = (type((1,)), type([1]))
      self.hit, self.diff = 0, 0
      self.valStr = ''

   def __call__(self, seq, *args):
      
      if args in ((), (()), ([])):
         seq.sort()
         return None
      elif (len(args) == 1) and (type(args[0]) in self.seqTypes):
         self.vals = args[0]
      else:
         self.vals = args

      seq.sort(self.__comp__)
      
   def __comp__(self, this, that):

      self.hit, self.diff = 0, 0
      
      for val in self.vals:
         if type(val) in self.valTypes:
            # optimized for comparisons at level 1
            try:
               self.diff = cmp(this[val], that[val])
               self.hit = 1
            except:
               continue
            if self.diff:
               return self.diff
         elif type(val) in self.seqTypes:
            # generalized for comparisons at levels 2+
            self.valStr = ''
            for v in val:
               if type(v) == type(1):
                  self.valStr += "[%s]" % v
               elif type(v) == type('a'):
                  self.valStr += "[\'%s\']" % v
               else:
                  raise AttributeError, 'Nested arg must be int or string.'
            try:
               exec('self.diff = cmp(this%s, that%s)' % (self.valStr, self.valStr))
               self.hit = 1
            except:
               continue
            if self.diff:
               return self.diff
         else:
            raise AttributeError, 'Primary arg must be int, string, tuple, or list.'
         
      if self.hit:
         # all successful cmp() calls returned 0
         return 0
      else:
         # no successful cmp() calls
         raise ValueError, 'No args in common between compared objects.'

#
# test code
#

from random import randrange

dSort = DeepSort()

if __name__ == '__main__':

   tpls = [((randrange(0, 5, 1), randrange(0, 5, 1)), \
      (randrange(0, 5, 1), randrange(0, 5, 1))), \
      ((randrange(0, 5, 1), randrange(0, 5, 1)), \
      (randrange(0, 5, 1), randrange(0, 5, 1))), \
      ((randrange(0, 5, 1), randrange(0, 5, 1)), \
      (randrange(0, 5, 1), randrange(0, 5, 1))), \
      ((randrange(0, 5, 1), randrange(0, 5, 1)), \
      (randrange(0, 5, 1), randrange(0, 5, 1))), \
      ((randrange(0, 5, 1), randrange(0, 5, 1)), \
      (randrange(0, 5, 1), randrange(0, 5, 1))), \
      ((randrange(0, 5, 1), randrange(0, 5, 1)), \
      (randrange(0, 5, 1), randrange(0, 5, 1)))]
   
   dcts = [({'a':randrange(0, 5, 1),'b':randrange(0, 5, 1)}, \
      {'a':randrange(0, 5, 1),'b':randrange(0, 5, 1)}), \
      ({'a':randrange(0, 5, 1),'b':randrange(0, 5, 1)}, \
      {'a':randrange(0, 5, 1),'b':randrange(0, 5, 1)}), \
      ({'a':randrange(0, 5, 1),'b':randrange(0, 5, 1)}, \
      {'a':randrange(0, 5, 1),'b':randrange(0, 5, 1)}), \
      ({'a':randrange(0, 5, 1),'b':randrange(0, 5, 1)}, \
      {'a':randrange(0, 5, 1),'b':randrange(0, 5, 1)}), \
      ({'a':randrange(0, 5, 1),'b':randrange(0, 5, 1)}, \
      {'a':randrange(0, 5, 1),'b':randrange(0, 5, 1)}), \
      ({'a':randrange(0, 5, 1),'b':randrange(0, 5, 1)}, \
      {'a':randrange(0, 5, 1),'b':randrange(0, 5, 1)})]

   print
   print 'tpls:'
   print tpls
   print
   dSort(tpls)
   print 'dSort(tpls):'
   print tpls
   print
   dSort(tpls, 1, 0)
   print 'dSort(tpls, 1, 0):'
   print tpls
   print
   dSort(tpls, 0, 1)
   print 'dSort(tpls, 0, 1):'
   print tpls
   print
   dSort(tpls, (0, 1), (1, 0))
   print 'dSort(tpls, (0, 1), (1, 0)):'
   print tpls
   print
   dSort(tpls, [(1, 0), (0, 1)])
   print 'dSort(tpls, [(1, 0), (0, 1)]):'
   print tpls
   print
   print 'dcts:'
   print dcts
   print
   dSort(dcts)
   print 'dSort(dcts):'
   print dcts
   print
   dSort(dcts, 1, 0)
   print 'dSort(dcts, 1, 0):'
   print dcts
   print
   dSort(dcts, 0, 1)
   print 'dSort(dcts, 0, 1):'
   print dcts
   print
   dSort(dcts, (0, 'a'), (1, 'a'))
   print "dSort(dcts, (0, 'a'), (1, 'a')):"
   print dcts
   print
   dSort(dcts, ((1, 'a'), (0, 'a')))
   print "dSort(dcts, ((1, 'a'), (0, 'a'))):"
   print dcts
   print
