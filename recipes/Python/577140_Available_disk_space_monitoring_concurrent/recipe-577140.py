import os
import sys
import unittest
from multiprocessing.managers import SyncManager
from contextlib import contextmanager
__license__ = 'MIT'
__email__ = 'mat@miga.me'
#
#
#
class SharedDiskSpaceProctor(SyncManager):
   def __init__(self):
      SyncManager.__init__(self)
         self.register(	'DiskSpaceProctor',
               callable=DiskSpaceProctor,
               exposed=('_can_write', '_close_write', 'make_dirs'))
#
#
#
class DiskSpaceProctorException(Exception):
   def __init__(self,msg,**kwds):
      for k,v in kwds.items():
         setattr(self,k,v)
      self.msg = msg
   def __str__(self):
      return '%s - %s'%(self.msg, str(self.__dict__)) 

#
#
#
class DiskSpaceProctor(object):
   def __init__(self):
      self._wRLock = threading.RLock()
      self._currentWrites = {}
   #
   def _can_write(self, path, fz):
      '''
         returns True if there is available space and
         considers current write operations from other
         processes
      '''
      with self._wRLock:
         try:
            path = self.__chk_cwd(path) 
            s = os.statvfs(os.path.dirname(path))
            ca = s.f_frsize * s.f_bavail
            if self._currentWrites.has_key(path):
               raise DiskSpaceProctorException('Concurrent writes not allowed to same path%s'%path)
            wbt = 0
            for v in self._currentWrites.values():
               wbt += v
            if (fz + wbt) < ca:
               self._currentWrites[path]=fz
               return True
            raise DiskSpaceProctorException (
               'Raising Exception "%s" from %s.%s()'%(
                  'Not enough space for requested file size',
                  self.__class__.__name__, str(inspect.stack()[0][3]))
            )
         except DiskSpaceProctorException, de:
            raise de
         except Exception, e:
            raise Exception (
               'Raising Exception "%s" from %s.%s()'%(
                  e, self.__class__.__name__, str(inspect.stack()[0][3]))
            )
   #
   def _close_write(self, path):
      '''
         remove path and its filesz out of current writes addition
      '''
      with self._wRLock:
         path = self.__chk_cwd(path)
         self._currentWrites.pop(path)
   #
   def make_dirs(self, path, mode=0754, potFilesz=4096):
      '''
         create full path, consider potential file write sz
      '''
      if os.path.exists(path): return True
      if self._can_write(path, potFilesz):
         os.makedirs(path, mode=mode)
         self._close_write(path)
         return True
      return False
   #
   def __chk_cwd(self, path):
      return os.path.join(os.getcwd(),path) if os.path.dirname(path)=='' else os.path.dirname(path)
#
#
#  
class Test(unittest.TestCase):
   def test_diskspace_proctor(self):
      sdsp = SharedDiskSpaceProctor()
      sdsp.start()
      dsp = sdsp.DiskSpaceProctor()
      dspLock = sdsp.Lock()
      testFilename = 'diskspaceproctortest.dat'
      if os.path.exists(testFilename):
         os.remove(testFilename)
      doWrite = False
      with dspLock: 
         doWrite = dsp._can_write(testFilename, 4096):
      if doWrite:    
         f = open(testFilename, 'w')
         f.write('for testing only')
         f.close()
      self.assertTrue(os.path.exists(testFilename))   
#  
if __name__ == '__main__':
   unittest.main()
