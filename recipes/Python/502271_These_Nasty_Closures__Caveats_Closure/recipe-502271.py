'''
According to my expectations, the three functions in this code below should all
produce the same result. I've been stunned to discover that this is not the case.
'''

def test1():
   for i in range(5):
      def call(): return i
      yield call

def test2():
   all = []
   for i in range(5):
      def call(): return i
      all.append(call)
   return all

def test3():
   def MakeCall(i):
      def call(): return i
      return call

   all = []
   for i in range(5):
      all.append(MakeCall(i))
   return all


print
for test in [ test1, test2, test3 ]:
   print test.__name__, ':', [ f() for f in test() ]

expected_output = '''
test1 : [0, 1, 2, 3, 4]
test2 : [0, 1, 2, 3, 4]
test3 : [0, 1, 2, 3, 4]
'''
actual_output = '''
test1 : [0, 1, 2, 3, 4]
test2 : [4, 4, 4, 4, 4] # <= this is the stunning thing !!!
test3 : [0, 1, 2, 3, 4]
'''
