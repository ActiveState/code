import win32con 

# Definition des clef de registre
HKEY_CLASSES_ROOT = win32con.HKEY_CLASSES_ROOT 
HKEY_CURRENT_USER = win32con.HKEY_CURRENT_USER 
HKEY_LOCAL_MACHINE = win32con.HKEY_LOCAL_MACHINE
HKEY_USERS = win32con.HKEY_USERS


class RegistryFileError(Exception):
   def __init__(self):
      Exception.__init__(self)
      
      
class FileNotFoundError(RegistryFileError):
   """ File not found error """
   def __init__(self,key,sub_key):
      RegistryFileError.__init__(self)
      self.key = key
      self.sub_key = sub_key
      
   def __str__(self):
      return 'No such registry file or directory %X:%s'%(self.key,self.sub_key)
      

class InvalidModeError(RegistryFileError):
   """ Invalid mode error ou mode unknown """
   def __init__(self, flag):
      RegistryFileError.__init__(self)
      self.flag = flag
      
   def __str__(self):
      return 'Invalid mode: %s'%self.flag
      
      
class BadFileDescriptorError(RegistryFileError):
   """ The cannot be read or write according to mode """
   def __init__(self):
      RegistryFileError.__init__(self)
      
   def __str__(self):
      return 'Bad registry file descriptor'


class RegistryFile:
   """ This class manage a file in a Win32 registry base """
   READ   = 1
   WRITE  = 2
   APPEND = 3
   
   def __init__(self, key, sub_key, flag):
      """
Constructor :
   key     : HKEY_CLASSES_ROOT, HKEY_CURRENT_USER, HKEY_LOCAL_MACHINE, HKEY_USERS
   sub_key : The name of a key that this method opens
   flag    : "r" for read
             "w" for write
             "a" for append
             "b" for binary
      """
      from win32api import RegQueryValueEx, RegCreateKey, RegOpenKeyEx
      from win32con import KEY_ALL_ACCESS
      from StringIO import StringIO
      
      # Save files informations
      self.key = key
      self.sub_key = sub_key
      
      # Initialization of internal data
      self.deleted = 0
      self.handle = None
      self.data = None
      
      # Check mode
      self.__checkMode(flag)
      
      # Create an empty file
      self.data = StringIO()
      
      try:
         # Open registry key
         self.handle = RegOpenKeyEx(key,sub_key,0,KEY_ALL_ACCESS)
         
         # Read key content
         data = RegQueryValueEx(self.handle, "")[0]
         
         # If the file is in read mode
         if self.flag == self.READ:
            # Read data
            self.data = StringIO(data)
         # If the file is in append mode
         elif self.flag == self.APPEND:
            self.data.write (data)
      except:  # If the registry key not found
         # If the file must be read
         if self.flag == self.READ:
            # The file is not found
            raise FileNotFoundError(key,sub_key)
         else:
            # Create a new registry key
            self.handle = RegCreateKey(key, sub_key)
      
   def __del__(self):
      """ Destructor """
      self.close()
      
   def __checkMode(self, flag):
      """ Check the file mode """
      from string import lower
      self.binary = 0
      
      for i in flag:
         try:
            # Obtain flag
            self.flag = {"r":self.READ,"w":self.WRITE,"a":self.APPEND}[lower(i)]
         except:
            # If binary file selected
            if lower(i) == "b":
               # Set binary file
               self.binary = 1
            else:
               # Invalid mode
               raise InvalidModeError(flag)
         
   def __checkRead(self):
      """ Check if the file can be read """
      if self.flag != self.READ:
         raise BadFileDescriptorError
         
   def __checkWrite(self):
      """ Check if the file can be writed """
      if not self.flag in (self.WRITE,self.APPEND):
         raise BadFileDescriptorError
         
   def close(self):      
      """ Close file and write in registry """
      from win32con import REG_SZ, REG_BINARY
      from win32api import RegSetValueEx
      
      # If the file has been opened correctly
      if self.handle != None and self.data != None:
         # If the file has not been deleted
         if self.deleted == 0:
            # If the file is opened with binary mode
            if self.binary:
               typ = REG_BINARY
            else:
               typ = REG_SZ
            
            # Write data in registry base
            RegSetValueEx (self.handle, "", 0, typ, self.data.getvalue())
         
         # Close file
         result = self.data.close()
         self.data = None
         return result
   
   def delete(self):
      """ Delete the registry file """
      from win32api import RegDeleteKey
      
      # Destroy file
      RegDeleteKey(self.key, self.sub_key)
      self.deleted = 1
      
   def isatty(self):     
      return self.data.isatty()
      
   def seek(self, pos, mode = 0):
      return self.seek(pos, mode)

   def tell(self):
      return self.data.tell()

   def read(self, size = -1):
      self.__checkRead()
      return self.data.read(size)

   def readline(self, length=None):
      self.__checkRead()
      return self.data.readline(length)

   def readlines(self, sizehint = 0):
      self.__checkRead()
      return self.data.readlines(sizehint)

   def truncate(self, size=None):
      self.__checkWrite()
      return self.data.truncate(size)

   def write(self, s):
      self.__checkWrite()
      return self.data.write(s)

   def writelines(self, list):
      self.__checkWrite()
      return self.data.writelines(list)

   def flush(self):
      self.__checkWrite()
      return self.data.flush()

      
import unittest
class RegistryFileTest(unittest.TestCase):
   def testFileNotFoundError(self):
      self.assertRaises(FileNotFoundError, RegistryFile, HKEY_LOCAL_MACHINE,"Software\\NotFound","r")
      
   def testInvalidModeError(self):
      self.assertRaises(InvalidModeError, RegistryFile, HKEY_LOCAL_MACHINE,"Software\\NotFound","z")
      
   def testWriteNormalFile(self):
      from time import sleep
      RegistryFile(HKEY_LOCAL_MACHINE,"Software\\RegistryFileTest","w").write("toto\0")
      self.assertEqual(RegistryFile(HKEY_LOCAL_MACHINE,"Software\\RegistryFileTest","r").read(),"toto")

   def testWriteBinaryFile(self):
      RegistryFile(HKEY_LOCAL_MACHINE,"Software\\RegistryFileTest","wb").write("toto\0")
      self.assertEqual(RegistryFile(HKEY_LOCAL_MACHINE,"Software\\RegistryFileTest","rb").read(),"toto\0")
         
   def testWriteAllBinaryCode(self):
      buf = ""
      for i in range(0,256):
         buf += chr(i%256)
      RegistryFile(HKEY_LOCAL_MACHINE,"Software\\RegistryFileTest","wb").write(buf)
      self.assertEqual(RegistryFile(HKEY_LOCAL_MACHINE,"Software\\RegistryFileTest","rb").read(),buf)
      
   def testWriteReadLines(self):
      buf = ["Line1\n","Line2\n","Line3\n"]
      RegistryFile(HKEY_LOCAL_MACHINE,"Software\\RegistryFileTest","w").writelines(buf)
      self.assertEqual(RegistryFile(HKEY_LOCAL_MACHINE,"Software\\RegistryFileTest","r").readlines(),buf)
      
   def testZDeleteFile(self):
      RegistryFile(HKEY_LOCAL_MACHINE,"Software\\RegistryFileTest","r").delete()
      self.assertRaises(FileNotFoundError, RegistryFile, HKEY_LOCAL_MACHINE,"Software\\RegistryFileTest","r")

def sample():
   file = RegistryFile(HKEY_LOCAL_MACHINE,"Software\\RegistryFileTest","w")
   file.write ("Hello world")
   del(file)
   file = RegistryFile(HKEY_LOCAL_MACHINE,"Software\\RegistryFileTest","r")
   print file.read()
   file.delete()
   

if __name__ == "__main__":
   sample()
   unittest.main()
