# Class to encapsulate a progress indicator

import sys, os

import unittest 

class progressException(Exception): 'Error to raise for any recursive problem.' 

class progress: 

   def __init__ (self): 
      self._twissler = ["|","/","-","\\","|"]
      self._state = 0 
   
   def getStart(self):
      sys.stdout.write('\t[  ') # include 2 spaces for the twissler
      sys.stdout.flush()
      
   def getStart(self, text):
      sys.stdout.write('\t %s [  ' % (text)) # include 2 spaces for the twissler
      sys.stdout.flush()   
   
   def moveOn(self): 
      try:          
         self._state = self._state + 1
         if self._state >= 5:
            self._state = 1                             
         sys.stdout.write( chr(8)+chr(8)+self._twissler[self._state]+']' )
         sys.stdout.flush()             
      except: 
         raise progressException('failed to progress') 
   
   

class TestCase(unittest.TestCase): 
   def setUp(self): 
      pass 
   def tearDown(self): 
      pass 
   def testProgress(self): 
      p = progress()       
      p.getStart()
      for a in range(0,10,1):                                          
         p.moveOn()
         time.sleep(0.2)
      
if __name__ == '__main__': 
   widgetTestSuite = unittest.TestSuite() 
   widgetTestSuite.addTest(TestCase("testProgress")) 
   runner = unittest.TextTestRunner() 
   runner.run(widgetTestSuite) 
