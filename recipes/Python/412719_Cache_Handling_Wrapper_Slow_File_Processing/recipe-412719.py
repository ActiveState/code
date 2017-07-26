# *** Put this in "fcache.py" ***

import sys, os
try:
   import cPickle as pickle
except ImportError:
   import pickle

######################################################################
## 
## File Utilities
## 
######################################################################

def ftime(filename, default=-sys.maxint):
   if os.path.isfile(filename):
      return os.path.getmtime(filename)
   return default

def fisnewer(path, thenpath):
   return ftime(path) > ftime(thenpath)

def fstem(filename):
   return os.path.splitext(os.path.basename(filename))[0]

def fpickle(filename, content):
   if __debug__: print '==> pickling content to %s' % fstem(filename)
   file = open(filename, 'wb')
   try:
      try:
         pickle.dump(content, file, True)
      finally:
         file.close()
   except:
      os.remove(filename)
      raise

def funpickle(filename):
   if __debug__: print '==> unpickling content from %s' % fstem(filename)
   file = open(filename, 'rb')

   try:
      return pickle.load(file)
   finally:
      file.close()

######################################################################
## 
## Introspection Helpers
## 
######################################################################


def definingModuleFile(func):
   return func.func_code.co_filename

def definingModuleName(func):
   return fstem(definingModuleFile(func))

def qualifiedIdentifier(func):
   m = definingModuleName(func)
   try:
      c = func.im_class
   except AttributeError:
      return '%s.%s' % (m, func.__name__)
   else:
      return '%s.%s.%s' % (m, c.__name__, func.__name__)

def defaultCacheDirectory():
   return os.path.join(os.path.dirname(__file__), '@cache')

######################################################################
## 
## Encoding Functions used to generate a cache file name
## 
######################################################################

def hashhex(s):
   return hex(hash(s))[2:]

def md5hex(s):
   import md5
   return md5.new(s).hexdigest()

######################################################################
## 
## Cache Handling
## 
######################################################################

def cacheFileStem(func, args, encode=hashhex):
   id = encode(repr(args))
   return r'%s-%s' % (qualifiedIdentifier(func), id)

def shouldRebuild(target, sources):
   for each in sources:
      if fisnewer(each, target): return True
   return False

class CacheManager:
   def __init__(self, cacheDir=None, cacheFileExt='.cache', encode=hashhex):
      self._dir = cacheDir or defaultCacheDirectory()
      if not os.path.isdir(self._dir): os.makedirs(self._dir)
      self._ext = cacheFileExt
      self._encode = encode
      self._cachefiles = []
   def cacheFilePath(self, func, *args):
      filename = cacheFileStem(func, args, encode=self._encode)
      return os.path.join(self._dir, filename) + self._ext
   def deleteCacheFiles(self):
      for each in self._cachefiles[:]:
         if os.path.isfile(each):
            os.remove(each)
            self._cachefiles.remove(each)
   def wrap(self, func):
      def call(*sources):
         sources = map(os.path.abspath, sources)
         cachefile = self.cacheFilePath(func, *sources)
         if shouldRebuild(cachefile, sources):
            result = func(*sources)
            fpickle(cachefile, result)
            self._cachefiles.append(cachefile)
         else:
            result = funpickle(cachefile)
         return result
      return call


# --------------------------------------------------------------------
# *** Put this in a separate file, say "fcache_test.py" ***

if __name__ == '__main__':
   import sys
   import fcache

   # create source files
   for i in range(1, 5): open('file%d.txt' % i, 'wt').close()

   # define a processing function
   def processFiles(file1, file2):
      s = 'processing files %r and %r ...' % (file1, file2)
      print s
      return s

   # define a processing method
   class FileProcessor:
      def processFiles(self, file1, file2):
         return processFiles(file1, file2)

   processor = FileProcessor()

   # create a cache manager
   cm = fcache.CacheManager()

   # let's have a look at the generated cache file names
   print
   print fcache.cacheFileStem(processFiles, ('file1.txt', 'file2.txt'), encode=fcache.hashhex)
   print fcache.cacheFileStem(processor.processFiles, ('file1.txt', 'file2.txt'), encode=fcache.hashhex)

   # wrap the processing function
   f = cm.wrap(processFiles)

   # see what happens when a function is repeatedly again with the same arguments
   print
   result = f('file1.txt', 'file2.txt'); print 'result:', result
   result = f('file3.txt', 'file4.txt'); print 'result:', result
   result = f('file1.txt', 'file2.txt'); print 'result:', result
   result = f('file1.txt', 'file2.txt'); print 'result:', result

   # delete this sessions cache files, if you don't need them later
   # (normaly, you would leave them for later recycling)
   cm.deleteCacheFiles()

   # delete test source files
   for i in range(1, 5): os.remove('file%d.txt' % i)

# --------------------------------------------------------------------
