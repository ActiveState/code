def intersection(set1, set2, *args):
   """
   Returns intersection of tuples/lists of data, where

   1) the number of sets is greater than 1,
   2) the dimensionality of the sets is not pre-defined,
       s1 = [(1,), 'e', [[1, 7], (4L, 3j, ('', None))], ([2], {'a': 'b'})]
   3) the sets are not required to share common dimensionality,
       s2 = (1, 2, 3, None)
   4) the returned object is a one-dimensional list of objects which are
      neither TupleType nor ListType and has no duplicates.
       intersection(s1, s2) == [1, 2, None]
   """
   result = []
   sets = []
   sets_append = sets.append
   result_append = result.append

   sets_append(union(set1))
   sets_append(union(set2))

   for arg in args:
      sets_append(union(arg))

   for obj in sets[0]:
      for i in range(1, len(sets), 1):
         hit = obj in sets[i]
         if not hit:
            break
      if hit:
         result_append(obj)

   return compact(result)

def union(*args):
   """
   Returns union of tuples/lists of data, where

   1) the dimensionality of the sets is not pre-defined,
       s1 = [(1,), 'e', [[1, 7], (4L, 3j, ('', None))], ([2], {'a': 'b'})]
   2) the sets are not required to share common dimensionality,
       s2 = (1, 2, 3, None)
   3) the union of one set is the set stripped of duplicates,
   4) the returned object is a one-dimensional list of objects which are
      neither TupleType nor ListType and has no duplicates.
       union(s1) == [{'a': 'b'}, 'e', 3j, None, 4L, 7, 2, 1, '']
       union(s1, s2) == [{'a': 'b'}, 'e', 3j, None, 4L, 7, 3, 2, 1, '']
   """
   result = []
   sequenceSet = (type([1]), type((1,)))
   result_extend = result.extend
   result_append = result.append

   for arg in args:
      if type(arg) in sequenceSet:
         for obj in arg:
            result_extend(union(obj))
      else:
         result_append(arg)

   return compact(result)

def compact(sequence):
   """
   Returns list of objects in sequence sans duplicates, where
    s1 = (1, 1, (1,), (1,), [1], [1], None, '', 0)
    compact(s1) == [[1], 1, 0, (1,), None, '']
   """
   result = []
   dict_ = {}
   result_append = result.append

   for i in sequence:
      try:
         dict_[i] = 1
      except:
         if i not in result:
            result_append(i)

   result.extend(dict_.keys())

   return result
