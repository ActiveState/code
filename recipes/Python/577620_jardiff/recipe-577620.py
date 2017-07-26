#!/usr/bin/python
#
# Author  : Raphael Jolivet
# Release : 22-mar-2011
import sys
import re
from zipfile import ZipFile
from fnmatch import fnmatch
from StringIO import StringIO

# ----------------------------------------------------------------------------
# Class IgnoreRules
# ----------------------------------------------------------------------------
 
""" 
Ignore Rules class. 
Made of list of 'glob' filename pattern to ignore whole files,
and a dictionnary of <'glob' filename patterns> => [list of regexp patterns] to ignore some lines in specific text files.
"""
class IgnoreRules :
    def __init__(
        self, 
        ignoreFiles = [], # List of file patterns to ignore (ala 'glob' with ? and * wildcards) 
        ignorePatternsPerFile = {} # Map of <file glob pattern> => [list of regexp patterns] for lines to ignore in some text files 
    ) :

        self.ignoreFiles = ignoreFiles

        # List of regexp patterns to ignore in some files (with ? and * patterns in filenames)
        # Compile the patterns
        self.ignorePatternsPerFile = {}
        for key in ignorePatternsPerFile.keys() :
            self.ignorePatternsPerFile[key] = []
            for pattern in ignorePatternsPerFile[key] :
                self.ignorePatternsPerFile[key].append(re.compile(pattern))


# ----------------------------------------------------------------------------
# Config
# ----------------------------------------------------------------------------

RULES = IgnoreRules( 
                
        # Ignored files
        [
            "*/README.txt",
            "*.java" # Source files
         ],  

        # Lines ignored in text files
        { 
            # Version information within manifests
            "META-INF/MANIFEST.MF" : [
                '^Implementation-Version\s*:.*$',
                '^Implementation-Build-Time\s*:.*$',
                '^Implementation-Revision\s*:.*$'],
            
            # Comments within INI files : "; Blabla"    
            "*.ini" : [
                '^\s*;.*$']
        }
)
      
# ----------------------------------------------------------------------------
# Main method
# ----------------------------------------------------------------------------

"""
    Diff between two zipfiles
    Returns None if files are the same
    Return a string describing the first diff encountered otherwise
"""
def diffZips(zip1, zip2, ignoreRules) :
   
    # Build maps of entries
    zip1Map = {}
    for entry in zip1.infolist() :
        zip1Map[entry.filename] = entry
    zip2Map = {}
    for entry in zip2.infolist() :
        zip2Map[entry.filename] = entry

    # Check we have same list of files
    zip1KeySet = set(zip1Map.keys())
    zip2KeySet = set(zip2Map.keys())

    if zip1KeySet != zip2KeySet :
        return "Different list of entries" + zip1KeySet.symmetric_difference(zip1KeySet)
    
    # Loop on entries
    for filename in zip1KeySet :

        # Is it a folder => Then no diffs, its ocntents will be checked anyway
        if filename.endswith('/') : continue

        # Get each entry
        entry1 = zip1Map[filename]
        entry2 = zip2Map[filename]

        # Is it a bundled zip ?
        if fnmatch(filename, "*.zip") or fnmatch(filename, "*.war") or fnmatch(filename, "*.jar") :
           
            # Same CRC and size ? They are identic : No need to look into it
            if entry1.file_size == entry2.file_size and entry1.CRC == entry2.CRC : continue 

            # Open the files as ZipFiles
            subZip1 = ZipFile(StringIO(zip1.read(entry1)))
            subZip2 = ZipFile(StringIO(zip2.read(entry2)))

            # Recursively diff them
            diff = diffZips(subZip1, subZip2, ignoreRules)

            # Close zip files
            subZip1.close()
            subZip2.close()

            # Diff found => exit
            if diff != None : return "In %s : %s" % (filename, diff)

            # No diff here : skip no next one
            continue

        # Do we ignore this file ?
        ignore = False
        for pattern in ignoreRules.ignoreFiles :
            if fnmatch(filename, pattern) :
                ignore = True
                break
        if ignore : continue # File ignored => check next entry

        # Is it a text file ?
        textFile = False
        for pattern in ignoreRules.ignorePatternsPerFile.keys() :
            if fnmatch(filename, pattern) :
         
                textFile = True

                # Open the files and check their lines
                file1 = zip1.open(entry1) 
                file2 = zip2.open(entry2) 
                result = diffTextFiles(
                    file1, 
                    file2,
                    ignoreRules.ignorePatternsPerFile[pattern])

                file1.close()
                file2.close()
                if result != None :
                    return "Text files %s are not the same : %s" % (filename, result)
                else :
                    break

        # This was a text file ? => already checked => continue
        if textFile : continue
        
        # -- Binary file ?

        # Check size
        if entry1.file_size != entry2.file_size :
            return "Entry '%s' has different sizes : %d <> %d" % (filename, entry1.file_size, entry2.file_size)

        # Check CRC 
        if entry1.CRC != entry2.CRC :
            return "Entry '%s' has different CRCs : %s <> %s" % (filename, entry1.CRC, entry2.CRC)
        #else :
        #    print "File %s CRC1=%s, CRC2=%s" % (filename, entry1.CRC, entry2.CRC)
        # End of loop on entries
 
    # No diff found here
    return None


# Diff two text files, 
# Ignoring some lines
# return None if files are identic, a string describing the diff otherwise
def diffTextFiles(file1, file2, ignorePatterns) :

    lineNo = 0
    while True :

        # Get next lines
        line1 = file1.readline().strip()
        line2 = file2.readline().strip()        
        lineNo += 1

        # We reached the end
        if len(line1) == 0 and len(line2) == 0 : return None
        
        # Replace ignore patterns
        for pattern in ignorePatterns :
            if pattern.match(line1) != None :
                line1 = "#IGNORED"
            if pattern.match(line2) != None :
                line2 = "#IGNORED"

        if line1 != line2 : return "Line %d differ : '%s' <> '%s'" % (lineNo, line1, line2)
        

# --------------------------------------------------------------------
# Main
# --------------------------------------------------------------------
if __name__ == "__main__":
  
    # Get arguments, create zipfiles
    zip1 = ZipFile(sys.argv[1], 'r')
    zip2 = ZipFile(sys.argv[2], 'r')
    
    # Diff zipfiles
    result = diffZips(
        zip1,
        zip2,
        RULES)
    
    # If diff : print diff description, status=1
    # If no diff : print nothing, status=1 
    if result == None :
        sys.exit(0)
    else:
        print result
        sys.exit(1)
