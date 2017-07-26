def find_map_gen(main_list,pattern):
   """each call of next() method of this generator
   yields next index of main_list where pattern matches main_list[index]
   or raise StopIteration if there isn't next match
   
   main_list elements and pattern are maps with identical structure,
   pattern can have less keys
   
   meaning of 'match' need to be defined on your match function
   which have to compare value of pattern[key] with each element[key]
   and return list of True|False values for each element of main_list.
   It's up to you if match function does exact matching or for ex.
   for strings values pattern matching. All match fnc have to do is
   return for given key the list [first_elem_matches, second_elem_don't, ...]
   in True|False form, of course.

   """
   def varzip(a):
     return zip(*a)
 
   match_key_list = []
   true_tuple = tuple([True]*len(pattern))
   for key in pattern.keys():
      match_key_list.append(match(key,pattern,main_list))
   match_index_list = varzip(match_key_list)
   find_list = [true_tuple==x for x in match_index_list]
   for i,x in enumerate(find_list):
      if x: yield i


# example of use

find_gen = find_map_gen(my_list,pattern)
try:
   id = find_gen.next()
   print 'found %s -th record' % id+1
except StopIteration:
   print 'no more'

# very very simple example

>>> def match(key,pattern,list):
...   pattern_val = pattern[key]
...   return [pattern_val == elem[key] for elem in list]

>>> my_list = [{'a':1,'b':2, 'c':3}, {'a':1, 'b':6, 'c':4}]
>>> # all elems where a is 1
>>> pattern = {'a':1}
>>> find_gen = find_map_gen(my_list,pattern)
>>> print find_gen.next()
0                                # my_list[0] matches
>>> print find_gen.next()
1                                # my_list[1] matches too
>>> print find_gen.next()
Traceback (most recent call last):
  File "<stdin>", line 1, in ?
StopIteration                    # no more matches
>>>
>>> # all elems where a is 1 and c is 4
>>> pattern = {'a':1, 'c':4}
>>> find_gen = find_map_gen(my_list,pattern)
>>> print find_gen.next()
1                                # my_list[1] matches
>>> print find_gen.next()
Traceback (most recent call last):
  File "<stdin>", line 1, in ?
StopIteration                    # no more matches
>>>
>>> all elems with b is 7
>>>  pattern = {'b':7}
>>> find_gen = find_map_gen(my_list,pattern)
>>> print find_gen.next()
Traceback (most recent call last):
  File "<stdin>", line 1, in ?
StopIteration                    # no matches found
