import os.path
import fnmatch
import fileinput
import re
import string

def callback(arg, directory, files):
    for file in files:
        if fnmatch.fnmatch(file,arg):
            for line in fileinput.input(os.path.abspath(os.path.join(directory, file)),inplace=1):
                if re.search('.*theunderdogs.*', line): # I changed * to .* but it would probably work without this if
                    line = string.replace(line,'theunderdogs','the-underdogs') # old string , new string
                print line,
            

os.path.walk("c:/windows/favorites", callback, "*.url") # Directory  you are looking under, and file pattern
