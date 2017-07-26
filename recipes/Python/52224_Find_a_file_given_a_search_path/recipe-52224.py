from os.path import exists, join
from os import pathsep
from string import split

def search_file(filename, search_path):
   """Given a search path, find file
   """
   file_found = 0
   paths = string.split(search_path, pathsep)
   for path in paths:
      if exists(join(path, filename)):
          file_found = 1
          break
   if file_found:
      return abspath(join(path, filename))
   else:
      return None

if __name__ == '___main__':
   search_path = '/bin' + pathsep + '/usr/bin'  # ; on windows, : on unix
   find_file = search_file('ls',search_path)
   if find_file:
      print "File found at %s" % find_file
   else:
      print "File not found"
