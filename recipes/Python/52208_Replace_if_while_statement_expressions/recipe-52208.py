Before:

if i < 1:
   doSomething()

After:

if 0: # i< 1
   doSomething()
