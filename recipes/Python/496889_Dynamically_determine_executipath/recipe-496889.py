import os, sys, inspect
def execution_path(filename):
  return os.path.join(os.path.dirname(inspect.getfile(sys._getframe(1))), filename)

# open a file in a test
open(execution_path('sample.txt')).read()

# get the absolute path of the file
os.path.abspath(execution_path('sample.txt'))
