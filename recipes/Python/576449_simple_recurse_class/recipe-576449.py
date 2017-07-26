# Class to encapsualte building a file
# from a path
 
import sys, os, marshal, os.path, unittest
 
import unittest
 
class recursiveException(Exception):
    'Error to raise for any recursive problem.'
class recurse:
    ''' Encapulation of utility functions for directory
    recursion or other scripts'''
 
    def __init__ (self):
        # set any global state
        self.results = {'start_path': [], 'path_list': [], 'bad_paths': [], 'file_list': [] }
        self.stop_list = []
 
    def __init__ (self, stop_list):
        # set any global state
        self.results = {'start_path': [], 'path_list': [], 'bad_paths': [], 'file_list': [] }
        self.stop_list = stop_list
 
    def recurseDirs(self):
        try:
            self.results.get('path_list').append(os.getcwd())
            self.results.get('path_list').append(os.getcwd())
        except:
          raise recursiveException('failed to get any directories')
 
    def recurseDirsPath(self, path):
        try:
            self.results.get('start_path').append(path)
            self.__internalRecursePath(self.results.get('start_path')[0])
        except:
          raise recursiveException('failed to get any directories')
 

    def __internalRecursePath(self, path):
        parent = []
        # recursive call
        parent = os.listdir(path)
        #print parent
        for child in parent:
            if os.path.isfile(os.path.join(path, child)) and child[0] != '.':
               if not len(self.stop_list) == 0:
                       stop_child = True
                       for stop in self.stop_list:
                                if stop in child:
                                        stop_child = False
                       if not stop_child:
                                self.results.get('file_list').append(os.path.join(path, child)) # is file add to file list
               else:
                       if not '.jar' in child:
                                if not '.class' in child:
                                        self.results.get('file_list').append(os.path.join(path, child)) # is file add to file list
            if os.path.isdir(os.path.join(path, child)) and child[0] != '.' and child != 'RCS':
                #print os.path.join(path, child)
                self.results.get('path_list').append(os.path.join(path, child)) # else recurse the directories checking for more files
                self.__internalRecursePath(os.path.join(path, child))
 
    def somethingElse(self):
        print self.results
 
    def getAllPaths(self):
        return self.results
 
    def getAllFiles(self):
        return self.results.get('file_list')

class TestCase(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass
    def testRecurrsion(self):
        p = recurse([])
        p.recurseDirs()
    def testSomethingElse(self):
        p = recurse([])
        p.somethingElse()
    def testReturn(self):
        p = recurse([])
        p.recurseDirs()
        print p.getAllPaths()
    def testPath(self):
        p = recurse([])
        p.recurseDirsPath('/home/blogsj/simple')
        print p.getAllPaths()
    def testFile(self):
        p = recurse(['.zip', '.txt', '.html', '.pyc', '.pyo', '~'])
        p.recurseDirsPath('/home/blogsj/simple')
        for f in p.getAllFiles():
                print f
if __name__ == '__main__':
        widgetTestSuite = unittest.TestSuite()
        widgetTestSuite.addTest(TestCase("testRecurrsion"))
        widgetTestSuite.addTest(TestCase("testSomethingElse"))
        widgetTestSuite.addTest(TestCase("testReturn"))
        widgetTestSuite.addTest(TestCase("testPath"))
        widgetTestSuite.addTest(TestCase("testFile"))
        runner = unittest.TextTestRunner()
        runner.run(widgetTestSuite)
