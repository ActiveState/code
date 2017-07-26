#!/usr/bin/python
#
# relpath.py
# R.Barran 30/08/2004

import os

def relpath(target, base=os.curdir):
    """
    Return a relative path to the target from either the current dir or an optional base dir.
    Base can be a directory specified either as absolute or relative to current dir.
    """

    if not os.path.exists(target):
        raise OSError, 'Target does not exist: '+target

    if not os.path.isdir(base):
        raise OSError, 'Base is not a directory or does not exist: '+base

    base_list = (os.path.abspath(base)).split(os.sep)
    target_list = (os.path.abspath(target)).split(os.sep)

    # On the windows platform the target may be on a completely different drive from the base.
    if os.name in ['nt','dos','os2'] and base_list[0] <> target_list[0]:
        raise OSError, 'Target is on a different drive to base. Target: '+target_list[0].upper()+', base: '+base_list[0].upper()

    # Starting from the filepath root, work out how much of the filepath is
    # shared by base and target.
    for i in range(min(len(base_list), len(target_list))):
        if base_list[i] <> target_list[i]: break
    else:
        # If we broke out of the loop, i is pointing to the first differing path elements.
        # If we didn't break out of the loop, i is pointing to identical path elements.
        # Increment i so that in all cases it points to the first differing path elements.
        i+=1

    rel_list = [os.pardir] * (len(base_list)-i) + target_list[i:]
    return os.path.join(*rel_list)


--- 8< --- snip --- 8< --- snip --- 8< --- snip --- 8< ---

#!/usr/bin/python
#
# relpath_test.py
# R.Barran 30/08/2004

"""Unit test the relative path function"""

import relpath,unittest
import tempfile,os,shutil,sys


def FmtPath(testpath):
    """Format a file path in os.specific format"""
    return testpath.replace('/',os.sep)

def CreateTempFile(filename):
    f = open(filename,'w')
    f.close()


class relpath_tests(unittest.TestCase):
  
    def setUp(self):
        """Prepare test environment (basic setup shared by all tests)"""
        
        # Determine where the temp directory is and run the tests there
        self.TempDir = tempfile.gettempdir() + os.sep + 'relpath_tests_dir'
        try:
            shutil.rmtree(self.TempDir)
        except:
            pass
        os.mkdir(self.TempDir)
        os.chdir(self.TempDir)
        # Create directory structure
        os.makedirs('a/b/c/')
        os.makedirs('a1/b1/c1/d1')
        # Create a couple of files to point to
        CreateTempFile('file1')
        CreateTempFile('a/b/file2')
        CreateTempFile('a1/b1/c1/d1/file3')

    def tearDown(self):
        """Bin the temp test dir and everything in it"""
        os.chdir(self.TempDir)
        os.chdir(os.pardir)
        shutil.rmtree('relpath_tests_dir')
        
    #
    # Checking for valid input
    #
    
    def testInvalidTargetName(self):                                          
        """Should fail if the target does not exist """
        self.assertRaises(OSError, relpath.relpath, 'a/nofilehere.txt')

    def testNoTargetName(self):                                          
        """Should fail if the target is not supplied """
        self.assertRaises(OSError, relpath.relpath, '')

    def testInvalidBasePath(self):                                          
        """Should fail if the base path specified does not exist """
        self.assertRaises(OSError, relpath.relpath, 'file1', 'this/path/does/not/exist')
        
    def testBasePathIsNotADir(self):                                          
        """Should fail if the base is anything other than a directory """        
        self.assertRaises(OSError, relpath.relpath, 'file1', 'a/b/file2')

    def testTargetOnDifferentDrive(self):                                          
        """On windows platform the target must be on the same drive as the base point."""
        if sys.platform == 'win32':
            self.assertRaises(OSError, relpath.relpath, 'z:/file99')

    #
    # Tests with only the target specified (no base)
    #
    
    def testTargetinCurrDir(self):                                          
        """Target is in the current directory""" 
        self.assertEqual(relpath.relpath('file1'), 'file1')
        self.assertEqual(relpath.relpath(os.path.abspath('file1')), 'file1')

    def testTarget2DirsDown(self):                                          
        """Target is 2 directories down"""  
        self.assertEqual(relpath.relpath('a/b/file2'), FmtPath('a/b/file2'))
        self.assertEqual(relpath.relpath(os.path.abspath('a/b/file2')), FmtPath('a/b/file2'))

    def testTarget2DirsUp(self):                                          
        """Target is 2 directories up"""  
        os.chdir('a/b')      
        self.assertEqual(relpath.relpath('../../file1'), FmtPath('../../file1'))
        self.assertEqual(relpath.relpath(os.path.abspath('../../file1')), FmtPath('../../file1'))

    def testTarget2Up4Down(self):                                          
        """Target is 2 directories up then down 4"""
        os.chdir('a/b')      
        self.assertEqual(relpath.relpath('../../a1/b1/c1/d1/file3'), FmtPath('../../a1/b1/c1/d1/file3'))
        self.assertEqual(relpath.relpath(os.path.abspath('../../a1/b1/c1/d1/file3')), FmtPath('../../a1/b1/c1/d1/file3'))
        self.assertEqual(relpath.relpath(self.TempDir+'/a1/b1/c1/d1/file3'), FmtPath('../../a1/b1/c1/d1/file3'))

    #
    # Tests with target and base specified
    #

    def testTargetinCurrDir_c1(self):                                          
        """Target is in the current directory, base is in c1"""        
        self.assertEqual(relpath.relpath('file1','a1/b1/c1'), FmtPath('../../../file1'))
 
    def testTarget1DirUp_c1(self):                                          
        """Target is 1 directory up from current dir, base is in c1"""
        # Result should be same as previous test, this is just a way of checking that
        # changing the curr dir has no influence on the result. 
        os.chdir('a')      
        self.assertEqual(relpath.relpath(self.TempDir+'/file1',self.TempDir+'/a1/b1/c1'), FmtPath('../../../file1'))
 
    def testTarget2DirsDown_c1(self):                                          
        """Target is 2 directories down from current dir, base is in c1"""
        os.chdir('a')  
        self.assertEqual(relpath.relpath('b/file2',self.TempDir+'/a1/b1/c1'), FmtPath('../../../a/b/file2'))

    #
    # This final test is a bit different, it loops relpath 10000 times
    # and can be used for rough performance testing of different versions of
    # relpath
    #
    
    #def testSpeedTests(self):
        
    #    for i in range(10000):
    #        os.chdir(self.TempDir)
    #        self.assertEqual(relpath.relpath('file1','a1/b1/c1'), FmtPath('../../../file1'))
    #        self.assertEqual(relpath.relpath('a/b/file2'), FmtPath('a/b/file2'))
    #        os.chdir('a')  
    #        self.assertEqual(relpath.relpath('b/file2',self.TempDir+'/a1/b1/c1'), FmtPath('../../../a/b/file2'))

if __name__ == "__main__":
    unittest.main() 
    
    
