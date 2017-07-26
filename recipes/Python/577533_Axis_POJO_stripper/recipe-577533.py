import os, sys, shutil, tempfile, string
from os.path import join
"""
This utility lets us use the 'wsdl2java' utility from Axis-1 to 
generate POJOs from the schema embedded in a WSDL.  If we just want
POJOs without the Axis marshalling/unmarshalling code, then this
script will strip out the Axis code, leaving just the POJOs.

As of Axis-1.x, fortunately, all the Axis marshall/unmarshall code
is at the last part of the generated class files, so we can get away
with just truncating the file rather then truly parsing and performing 
an AST transformation. (i.e. don't need a real java parser)

Author: Chris Wolf cw10025 gmail com
"""

def stripAxisCode(fileName):
  """copy lines from in file to out file up to first occurance
     of the string 'org.apache.axis', then just write closing brace.
     hasAxisCode detects of the file was already processed such that
     this is an idempotent operation.
  """ 
  hasAxisCode = False
  fin = open(fileName, 'r')
  outName = ''.join([fileName, '.tmp'])
  fout = open(outName, 'wr')
  for line in fin:
    if (string.find(line, 'org.apache.axis') != -1 and
        string.find(line, 'extends') == -1 and
        string.find(line, 'implements') == -1):
      hasAxisCode = True
      break
    else:
      fout.write(line)

  fin.close() 
  if hasAxisCode:
    fout.write("}\n")
  fout.close
  shutil.move(outName, fileName)

def processDirTree(tld):
  """From the top level package dir of Axis-generated POJOs, 
     strip out Axis code to make just plain, old java objects 
     (real POJOs - without binding-specific marshalling guts)
  """
  for root, dirs, files in os.walk(tld):
    for name in files:
      stripAxisCode(join(root, name))


processDirTree(sys.argv[1])
