import sys

class case_selector(Exception):
   def __init__(self, value): # overridden to ensure we've got a value argument
      Exception.__init__(self, value)

def switch(variable):
   raise case_selector(variable)

def case(value):
   exclass, exobj, tb = sys.exc_info()
   if exclass is case_selector and exobj.args[0] == value: return exclass
   return None

def multicase(*values):
   exclass, exobj, tb = sys.exc_info()
   if exclass is case_selector and exobj.args[0] in values: return exclass
   return None

if __name__ == '__main__':
   print

   def InputNumber():
      while 1:
         try:
            s = raw_input('Enter an integer')
         except KeyboardInterrupt:
            sys.exit()
         try:
            n = int(s)
         except ValueError, msg:
            print msg
         else:
            return n

   while 1:
      n = InputNumber()
      try:
         switch(n)
      except ( case(1), case(2), case(3) ):
         print "You entered a number between 1 and 3"
      except case(4):
         print "You entered 4"
      except case(5):
         print "You entered 5"
      except multicase(6, 7, 8, 9):
         print "You entered a number between 6 and 9"
      except:
         print "Youe entered a number less then 1 or grater then 9"
