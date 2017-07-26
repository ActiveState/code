#!/usr/bin/env python

################################################################################
#                                                                              #
# Copyright (c) 2013, Mike 'Fuzzy' Partin <fuzzy@fu-manchu.org>                #
# All rights reserved.                                                         #
#                                                                              #
# Redistribution and use in source and binary forms, with or without           #
# modification, are permitted provided that the following conditions are met:  #
#                                                                              #
# 1. Redistributions of source code must retain the above copyright notice,    #
#    this list of conditions and the following disclaimer.                     #
# 2. Redistributions in binary form must reproduce the above copyright notice, #
#    this list of conditions and the following disclaimer in the documentation #
#    and/or other materials provided with the distribution.                    #
#                                                                              #
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"  #
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE    #
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE   #
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE     #
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR          #
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF         #
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS     #
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN      #
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)      #
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE   #
# POSSIBILITY OF SUCH DAMAGE.                                                  #
#                                                                              #
# The views and conclusions contained in the software and documentation are    #
# those of the authors and should not be interpreted as representing official  #
# policies, either expressed or implied, of the FreeBSD Project.               #
#                                                                              #
################################################################################

################################################################################
### Module imports                                                           ### 
################################################################################

# Stdlib
import os
import sys
import types
import ctypes

################################################################################
### libarchive.so detction and loading                                       ###
################################################################################

_LibPath = None
_LibDirs = [
  '/lib',
  '/lib32',
  '/usr/lib',
  '/usr/lib32',
  '/usr/pkg/lib',
  '/usr/pkg/lib32',
  '/usr/local/lib',
  '/usr/local/lib32'
]

def _setLibPath(a, d, f):
  ''' A private method used only as a callback for os.path.walk() '''
  global _LibPath
  if _LibPath == None:
    if 'libarchive.so' in f:
      _LibPath = d

## Next find libarchive.so
for path in _LibDirs:
  os.path.walk(path, _setLibPath, None)
if _LibPath == None:
  raise Exception('ERROR: Could not find libarchive.so on your system.')
    
## And since we have found it, lets load it
try:
  libarchive = ctypes.cdll.LoadLibrary('%s/libarchive.so' % _LibPath)
except OSError as msg:
  print(msg)
  sys.exit(1)


################################################################################
### libarchive FFI interface                                                 ###
################################################################################

class Libarchive:
  ''' Python CTypes interface to libarchive '''

  # These are our structs for libarchive (hopefully)
  class Archive(ctypes.Structure):
    pass

  class ArchiveEntry(ctypes.Structure):
    pass

  ##############################################################################
  ### Initialization                                                         ###
  ##############################################################################

  def __init__(self, fname=None, debug=False):
    ''' '''
    ##
    ## Setup our FFI interface
    ##
    ## Reference our global library handle
    global libarchive
    self.lib                    = libarchive

    ## Argument handling/setting
    self.__fname                = fname
    self.__debug                = debug

    ## Constants
    self.ARCH_EOF               = 1
    self.ARCH_OK                = 0
    self.ARCH_RETRY             = -10
    self.ARCH_WARN              = -20
    self.ARCH_FAILED            = -25
    self.ARCH_FATAL             = -30
    self.ExtractFlags           = 4 | 2 | 32 | 64 # TIME,PERM,ACL,FFLAGS
    
    ##
    ## Now we declare our function symbols and their return types
    ##
    ## Beginning with library version detection
    self.versionNumber          = self.lib.archive_version_number

    ## Pointer return types
    self._entryNew              = self.lib.archive_entry_new
    self._entryNew.restype      = ctypes.POINTER(self.ArchiveEntry)
    self._readNew               = self.lib.archive_read_new
    self._readNew.restype       = ctypes.POINTER(self.Archive)
    self._writeDiskNew          = self.lib.archive_write_disk_new
    self._writeDiskNew.restype  = ctypes.POINTER(self.Archive)

    ## Integer return types
    # Reading
    self._readClose             = self.lib.archive_read_close
    self._readDataBlock         = self.lib.archive_read_data_block
    self._readDataSkip          = self.lib.archive_read_data_skip
    self._readNextHeader        = self.lib.archive_read_next_header
    self._readOpenFilename      = self.lib.archive_read_open_filename
    self._readSupportFilterAll  = self.lib.archive_read_support_compression_all
    self._readSupportFormatAll  = self.lib.archive_read_support_format_all

    # Writing
    self._writeClose            = self.lib.archive_write_close
    self._writeDataBlock        = self.lib.archive_write_data_block
    self._writeDiskSetOptions   = self.lib.archive_write_disk_set_options
    self._writeDiskSetLookup    = self.lib.archive_write_disk_set_standard_lookup
    self._writeFinishEntry      = self.lib.archive_write_finish_entry
    self._writeHeader           = self.lib.archive_write_header
    # Info
    self._entrySize             = self.lib.archive_entry_size

    # This is due to a problem where libarchive version below v3.x do not have
    # the archive_read_free symbol. And archive_read_finish will only be kept
    # about until version 4 of the library, so no sense in not being forward
    # compatible about it.
    if int(self.versionNumber()) < int(3001002):
      self._readFree            = self.lib.archive_read_finish
      self._writeFree             = self.lib.archive_write_finish
    else:
      self._readFree            = self.lib.archive_read_free
      self._writeFree             = self.lib.archive_write_free

    ## String return types
    self._entryPathname         = self.lib.archive_entry_pathname
    self._entryPathname.restype = ctypes.c_char_p
    self._errorString           = self.lib.archive_error_string
    self._errorString.restype   = ctypes.c_char_p

  ##############################################################################
  ### Private methods                                                        ###
  ##############################################################################

  def _copyData(self, archiveR, archiveW):
    ''' '''
    r    = ctypes.c_int()
    buff = ctypes.c_void_p()
    size = ctypes.c_int()
    offs = ctypes.c_longlong()

    while True:
      # Read in a block
      r = self._readDataBlock(
        archiveR,           # Archive (reading)
        ctypes.byref(buff), # Buffer pointer
        ctypes.byref(size), # Size pointer
        ctypes.byref(offs)) # Offset pointer

      # Check ourselves
      if r == self.ARCH_EOF:
        return self.ARCH_OK
      if r != self.ARCH_OK:
        return r

      # Write out a block
      r = self._writeDataBlock(
        archiveW, # Archive (writing)
        buff,     # Buffer data
        size,     # Size data
        offs)     # Offset data
      
      # And check ourselves again
      if r != self.ARCH_OK:
        print(self._errorString(archiveB))
        return r

  def _fmtGauge(self, perc=None):
    ''' Display a 10 space progress bar '''
    buff = '[#'
    if perc and type(perc) == types.IntType:
      if (perc/10) > 0:
        for i in range(0,(perc/10)):
          buff += '#'
      for i in range(0,(10 - (perc / 10))):
        buff += '-'
      buff += ']'
      # and return our gauge
      return buff
    else:
      return None

  def _fmtTime(self, secs=None):
    ''' '''
    if secs and type(secs) in [types.IntType, types.LongType]:
      return '%ds' % secs

  def _fmtSize(self, size=None):
    ''' Format a number of bytes into a human readable string '''
    if size and type(size) in [types.IntType, types.LongType]:
      if size < 1024:
        return '%dB' % size
      elif size > 1024 and size < (1024**2):
        return '%4.02fKB' % (float(size) / 1024.00)
      elif size > (1024**2) and size < (1024**3):
        return '%4.02fMB' % ((float(size) / 1024.00) / 1024.00)
      else:
        return '%.02fGB' % (((float(size) / 1024.00) / 1024.00) / 1024.00)

  ##############################################################################
  ### Public methods                                                         ###
  ##############################################################################

  def listContents(self):
    ''' List the contents of the archive (returns a list of path/filenames) '''
    retv    = []               # Return value
    archive = self._readNew()  # Archive struct
    entry   = self._entryNew() # Entry struct

    # detect compression and archive type
    self._readSupportFilterAll(archive)
    self._readSupportFormatAll(archive)

    # Open, analyse, and close our archive
    if self._readOpenFilename(archive, self.__fname, 10240) != self.ARCH_OK:
      print(self._errorString(archive))
      sys.exit(1)

    while self._readNextHeader(archive, ctypes.byref(entry)) == self.ARCH_OK:
      retv.append(self._entryPathname(entry))
      self._readDataSkip(archive) # Not strictly necessary

    if self._readFree(archive) != self.ARCH_OK:
      print(self._errorString(archive))
      sys.exit(1)

    # Return our list of archive entries
    return retv

  def extractArchive(self):
    ''' '''
    # Get the number of elements in the archive (adds time on large archives)
    total     = len(self.listContents())
    processed = 0

    # Setup our structs
    arch      = self._readNew()
    ext       = self._writeDiskNew()
    entry     = self._entryNew()

    # detect archive type and compression
    self._readSupportFormatAll(arch)
    self._readSupportFilterAll(arch)

    # set our writer options
    self._writeDiskSetOptions(ext, self.ExtractFlags)
    self._writeDiskSetLookup(ext)

    # open the archive
    self._readOpenFilename(arch, self.__fname, 10240)

    # get our first header
    ret = self._readNextHeader(arch, ctypes.byref(entry))
    while ret != self.ARCH_EOF:
      if ret != self.ARCH_OK or ret < self.ARCH_WARN:
        print(self._errorString(arch))
        sys.exit(1)

      # write out our header
      ret = self._writeHeader(ext, entry)
      if ret != self.ARCH_OK:
        print(self._errorString(ext))
      elif self._entrySize(entry) > 0:

        # copy the contents into their new home
        self._copyData(arch, ext)
        if ret != self.ARCH_OK:
          print(self._errorString(ext))
        if ret < self.ARCH_WARN:
          sys.exit(1)
        processed += 1

        # And update our progress line
        sys.stdout.write('[1;32m>[0m Extracting %-46s %12s (%3d%%)\r' % (
          '%s:' % os.path.basename(self.__fname[:57]),
          self._fmtGauge(int((float(processed) / float(total)) * 100)),
          ((float(processed) / float(total)) * 100)
        ))
        sys.stdout.flush()

      # close that entry up
      ret = self._writeFinishEntry(ext)
      if ret != self.ARCH_OK:
        print(self._errorString(ext))
      if ret < self.ARCH_WARN:
        sys.exit(1)

      # And get ready to head back to the top
      ret = self._readNextHeader(arch, ctypes.byref(entry))

    # Cleanup
    self._readClose(arch)
    self._readFree(arch)
    self._writeClose(ext)
    self._writeFree(ext)

    # And one last update of our progress line
    sys.stdout.write('[1;32m>[0m Extracting %-46s %12s (%3d%%)\r' % (
      "%s:" % os.path.basename(self.__fname[:57]),
      self._fmtGauge(100),
      100
    ))
    sys.stdout.flush()    

    # You did good soldier
    return self.ARCH_OK

  def createArchive(self, files=None):
    ''' '''
    pass

################################################################################
### Main argument handling / operations                                      ###
################################################################################

if __name__ == '__main__':
  try:
    # Get rid of the program name argument(0)
    sys.argv.pop(0)
    # Chug through the remaining arguments and process them
    for arg in sys.argv:
      # First ensure that the argument is a valid file
      if os.path.exists(arg):
        obj = Libarchive(fname=arg)
        obj.extractArchive()
        print('')
      # Too bad, we don't exist, piss off
      else:
        raise Exception('ERROR: %s is not a valid filename.' % arg)
  # Lets print our message and get the hell outta here.
  except Exception as msg:
    print(msg)
    sys.exit(1)
