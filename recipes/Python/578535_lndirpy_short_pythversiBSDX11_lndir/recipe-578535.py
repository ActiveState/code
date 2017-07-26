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
import re
import sys
import types

################################################################################
### Main logic and argument handling                                         ###
################################################################################

try:
  if __name__ == '__main__':

    ### check to see that all args are present on the command line            
    ##############################################################
    if len(sys.argv) < 3:
      print("Usage: %s <src>/ <dst>/" % sys.argv[0])
      sys.exit(1)
    else:

      ### check to see that source and destination targets exist
      ##########################################################
      for i in [str(sys.argv[1]), str(sys.argv[2])]:
        if not os.path.isdir(i):
          raise OSError("ERROR: %s is not a valid directory." % i)

      ### Setup some convenience
      src     = str(sys.argv[1])
      dst     = str(sys.argv[2])
      src_b   = None

      if len(sys.argv) == 4:
        src_b = sys.argv[3]

      if src_b == None:
        if src[-1:] == '/':
          src_b = os.path.basename(src[:-1])
        else:
          src_b = os.path.basename(src)

      ### start walking the source target
      ###################################
      dirs_c = 0 # counter for dires
      file_c = 0 # counter for files
      for root, dirs, files in os.walk(src):
        for i in files:
          os.symlink('%s/%s'   % (root, i), 
                     '%s%s/%s' % (dst, re.sub(src, '', root), i))
          file_c += 1
        for i in dirs:
          try:
            os.mkdir('%s%s/%s' % (dst, re.sub(src, '', root), i))
          except OSError:
            pass
          dirs_c += 1
        sys.stdout.write('[1;32m>[0m %-53s %6d dirs %6d files\r' % (
          src_b[:52], # basename of src
          dirs_c,                          # Dir count
          file_c))                         # File count
        sys.stdout.flush()

  sys.stdout.write('[1;32m>[0m %-53s %6d dirs %6d files\n' % (
    src_b[:52], # basename of src
    dirs_c,  # Dir count
    file_c)) # File count
  sys.stdout.flush()
except OSError as msg:
  print(msg)
  sys.exit(0)
