def AreStringsIdentifiers(*strings):
   try:
      class test(object): __slots__ = strings
   except TypeError:
      return False
   else:
      return True

if __name__ == '__main__':
   print
   print AreStringsIdentifiers('A', 'B') # -> True
   print AreStringsIdentifiers('A', '1B', 'x y') # -> False
