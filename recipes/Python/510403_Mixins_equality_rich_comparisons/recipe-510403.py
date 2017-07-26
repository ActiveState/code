class KeyedEqualityMixin(object):
   def __eq__(self, other):
       return self.__key__() == other.__key__()
   def __ne__(self, other):
       return self.__key__() != other.__key__()

class KeyedComparisonMixin(KeyedEqualityMixin):
   def __lt__(self, other):
       return self.__key__() < other.__key__()
   def __le__(self, other):
       return self.__key__() <= other.__key__()
   def __gt__(self, other):
       return self.__key__() > other.__key__()
   def __ge__(self, other):
       return self.__key__() >= other.__key__()

class KeyedHashingMixin(KeyedEqualityMixin):
    def __hash__(self):
        return hash(self.__key__())


# =============================
# And at the interactive prompt
# =============================

>>> class C(object):
...     def __init__(self, x):
...         self.x = x
... 
>>> x, y, z = C(1), C(1), C(2)
>>> x == y, y < z, hash(x) == hash(y)
(False, False, False)
>>> class C(KeyedEqualityMixin):
...     def __init__(self, x):
...         self.x = x
...     def __key__(self):
...         return self.x
...        
>>> x, y, z = C(1), C(1), C(2)
>>> x == y, y < z, hash(x) == hash(y)
(True, False, False)
>>> class C(KeyedComparisonMixin):
...     def __init__(self, x):
...         self.x = x
...     def __key__(self):
...         return self.x
... 
>>> x, y, z = C(1), C(1), C(2)
>>> x == y, y < z, hash(x) == hash(y)
(True, True, False)
>>> class C(KeyedHashingMixin):
...     def __init__(self, x):
...         self.x = x
...     def __key__(self):
...         return self.x
... 
>>> x, y, z = C(1), C(1), C(2)
>>> x == y, y < z, hash(x) == hash(y)
(True, False, True)
