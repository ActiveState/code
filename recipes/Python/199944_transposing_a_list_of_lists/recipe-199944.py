>>> a=[[0,1],[0,1],[0,1]]
>>> print=zip(*a) #passes the lists in a as separate arguments 
[(0, 0, 0), (1, 1, 1)]
>>> print zip(*a)[0] #prints the first column
(0, 0, 0)

>>> a=[[0,1],[0,1,2],[0,1]] #lets see what happens when we use a "ragged" list
>>> print zip(*a) # the transpose is truncated to the shortest row
[(0, 0, 0), (1, 1, 1)]

>>> a=[[0,1],[0,1],[0,1],0] #What if there are not only lists in the list
>>> print zip(*a) #This does not work, so watch out for it.
Traceback (most recent call last):
  File "<interactive input>", line 1, in ?
TypeError: zip argument #4 must support iteration

>>> a=[(0,1),(0,1),(0,1)] #Does it work on a list of tuples?
>>> zip(*a) #Yes because a tuple is iterable.
[(0, 0, 0), (1, 1, 1)]
