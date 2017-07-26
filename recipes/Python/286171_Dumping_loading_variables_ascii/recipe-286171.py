#!/usr/bin/python

# Created by Karthikesh Raju < karthik@james.hut.fi >
# 
# Created: Sat 26 Jun 2004 12:45:35 PM EEST
# Last Modified: Thu 22 Jul 2004 08:28:17 PM EEST


"""
    This script loads a dictionary of tuples, array's (numarray) to a files. 
    The files are named after the keys of the dictionary (+-data.dat). If the 
    file contains complex data, the data is loaded into two files named 
    key-data-real/imag.dat.

    Given a directory containing a set of data files ('*.dat'), the script loads 
    all the files into a dictionary "result" with keys corresponding to the 
    principal file name. Files with real and imag names, are loaded into a 
    complex array. 
	
"""

# To Do:
# 1. How to handle dumping, if file already exists?
# 2. What about the ablity to individual variables with names and load
#    them into the primary workspace?
# 3. Load data with a file name or the directory.

__revision__ = "$Revision: 1.6$"

import numarray, tarfile 
import glob, string, os, time
import ConfigParser

def dumpData(data, fileName):
    """
	    Dumps the data into files. Complex Variables get dumped into files
	    varName-data-real.dat, varName-data-imag.dat.
        
        Usage:  
            data{'A'} = array([1,2,3,4])
            data{'B'} = array([1,2,3,4]) + 1j* array([1,2,3,4])
            data{'C'} = array([[1,2,3,4],[5,6,7,8]]) 
            dumpData(data)
            This creates files A-data.dat, B-data-real.dat, B-data-imag.dat, C-data.dat
    """
    try:
        print "Dumping Data:"
        # Keys become file names, so for each key, create a file.
        for key in data.keys():
            print ". ",
            
            # If the value corresponding to the key is complex,
            # create seperate files for the real and imag parts.
            if data[key].typecode() in ('D', 'F'):
                open1 = open(str(key) + '-data-real.dat', 'w')
                # Write real part to its corresponding file
                # by writeData function.
                writeData(open1, data[key].real)
                open1.close()
                
                open1 = open(str(key) + '-data-imag.dat', 'w')
                # Write imag part to its corresponding file
                # by writeData function.
                writeData(open1, data[key].imag)
                open1.close()
            else:
                # The data is real, so there is just one file 
                # created for the variable, and the data is
                # written into the corresponding file.
                open1 = open(str(key) + '-data.dat', 'w')
                writeData(open1, data[key])
                open1.close()
        
        print "\n"
		
        # Compress all the created files in an archive
        # with in today's date.
        files = glob.glob('*.dat')
        today = time.ctime()
        today = today.replace(' ', '-')
        today = today.replace(':', '-')
        compressName = fileName + today + '.tar.gz'
        compress(files, compressName)
    
    except AttributeError:
        # If the passed variable is not dictionary, print 
        # "only dictionaries are supported"
        print "Only dictionaries are supported. \n"


def loadData(dirName, archiveName):
    """
	    Given a dictionary, loadData loads all files with extension ".dat" into
        a dictionary. The keys of the dictionary are derived from the file names.
        Anything before -data-*.dat, forms the key for the dictionary.
        
        Usage:
            ~/test/A-data.dat
            ~/test/B-data-real.dat
            ~/test/B-data-imag.dat
            result = loadData('~/test')
        Result:
            result['A'] = array([1.,2.,3.,4.])
            result['B'] = array([1.+1.j,2.+2.j,3.+3.j,4.+4.j])
        Note:
            All data is converted into floats. So, the resultant matrix is a matrix of 
            floats, even if the original data is int.
    """
    
    # marker sets the starting part of the variable.
    # File names will be dirName/A-data.dat, so marker is the 
    # point where A-data.dat starts
    marker = len(dirName)+1
    
    if (dirName[-1] == "/" or archiveName[0] == "/"):
        archiveName = dirName + archiveName
    else:
        archiveName = dirName + "/" + archiveName
    
    uncompress(archiveName)
    
    # Choose only the extracted dat files
    dirName = dirName + '/*.dat'
    files = glob.glob(dirName)
    
    # Result holds the final dictionary
    result = {}
    
    # For each file in *.dat, separate the varaible which is
    # anything before -data-*. In the above case extract A from
    # A-data.dat. This is the key for the dictionary. 
    # 
    # Pass the file to the matrix creator which returns an array 
    # of the data
    
    print "Loading Data: "
    
    for name in files:
        print ". ",
        var = name.find('-')
        varName = name[marker:var] 
        
        varTypeReal = name.find('real')
        varTypeImag = name.find('imag')
        
        # file2matrix returns the contents of file "name" in an array
        value = file2matrix(name)
        os.remove(name)
        
        # If the key already exists, then this value should 
        # be either real or imag 
        if result.has_key(varName):
            if varTypeReal:     # real value
                result[varName] = value + 1j*result[varName] 
            elif varTypeImag:               # imag value
                result[varName] = result[varName] + 1j*value
        else:
            # If the key does not exist, then create an corresponding 
            # entry with the array "value" returned.
            result[varName] = value
        
    # "result", returned, contains the data in the files.
    return result

def file2matrix(fileName):
    """
        Given a file "fileName", this script converts the contents of the 
        file to a numarray matrix of size (m,) or (m,n).
    """
    # Open the file
    open1 = open(fileName, 'r')
    line = open1.readline()
    
    # A single line from the file is read. This should be the number
    # of columns. Spliting "line" results in a list, the length of 
    # which is the number of columns: cols
    cols = len(line.split())
    
    # x is the placeholder for the data.
    # The placeholder matrix is made of concatenating 
    # every line that is read from the file.
    # The type code is float. 
    x = numarray.zeros(cols, type='f')
  
    while (line):
        temp = []
        list_elements = line.split()
        for e in list_elements: 
            temp.append(float(e))
        x = numarray.concatenate((x, numarray.array(temp)))
        line = open1.readline()
    
    open1.close()
    
    # concatenate((x,x)) is along the dimension 1,
    # each new addition is an increase in columns,
    # the total length of x gives m*n. We determine
    # the rows as
    rows = len(x)/cols

    # We have added an aritifical row, so if row == 2
    # the file has tuple, hence the data consists of 
    # everything after our artificial set of columns
    if rows == 2:
        return x[cols:]
    else:
        # If there are m+1 rows, we resize the data to (m+1)xn
        # and return everything other than the artificial first
        # row of zeros
        x = numarray.resize(x, (rows, cols))
        return x[1:, :]


def writeData(fileHandle, data):
    """
        Given a handle to a file, and a matrix/tuple "data",
        the data is written to the file pointed to by "fileHandle".
        If "data" is a matrix, each row is a separate line. The
        file is of type string.
    """
	
    # If "data" is a matrix, each row forms a line.
    try:
        i, j = data.shape
        for ii in range(0, i):
            for jj in range(0, j):
                fileHandle.write("%s " %data[ii, jj])
            fileHandle.write('\n')
        fileHandle.write('\n')
    except ValueError:
        # If "data" is a tuple, there is just a row in the file.
        i = data.shape[0]
        for ii in range(0, i):
            fileHandle.write("%s " %data[ii])
        fileHandle.write('\n')

def compress(files, compressName):
    """
        Compress all the given files to a tar.gz archive
        Additionally remove all the given files (other than
        the archive) after compression.
    """
    tar = tarfile.open(compressName, "w:gz")
    for fileName in files:
        tar.add(fileName)
        os.remove(fileName)
    tar.close()
    
def uncompress(archiveFiles):
    """
        Given a archive file name, extract the contents of it
        in the current directory.
    """
    tar = tarfile.open(archiveFiles, "r:gz")
    for tarinfo in tar:
        tar.extract(tarinfo)
    tar.close()

class CaseConfigParser(ConfigParser.ConfigParser):
    """ A Case Sensitive Config Parser """
    def optionxform(self, optionstr):
        """ Overloading the returned optionstr to make it case sensitive """
        return optionstr
    
def loadConfig(fileName, config={}):
    """
        returns a dictionary with key's of the form
        <section>.<option> and the values
    """
    config = config.copy()
    cp = CaseConfigParser()
    cp.read(fileName)
    
    for sec in cp.sections():
        for opt in cp.options(sec):
            config[sec + "." + opt] = string.strip(cp.get(sec, opt))
            
    # The returned dictionary has the key of the form <section>.<option>
    # convertConfigDict converts every one of such form  to separate
    # dictionaries for each of the <section>.
    config = convertConfigDict(config)
    
    # For each value, convert all the possible numerical
    # values to float. The path names and other strings 
    # should remain the same
    for key in config.keys():
        for inKey in config[key].keys():
            try:
                config[key][inKey] = float(config[key][inKey])
                if (config[key][inKey] == int(config[key][inKey])):
                    config[key][inKey] = int(config[key][inKey])
            except ValueError:
                pass
                
    keys = config.keys()
    
    # The first dictionary should correspond to the source
    # and the second dictionary contains the parameters of
    # the jammer. Return the two dictionary.
    return config[keys[0]], config[keys[1]]

def convertConfigDict(origDict, sep="."):
    """
        For each key in the dictionary of the form <section>.<option>,
        a separate dictionary for is formed for every "key" - <section>,
        while the <option>s become the keys for the inner dictionary. 
        Returns a dictionary of dictionary.
    """
    result = {}
    for keys in origDict:
        tempResult = result
        parts = keys.split(sep)
        for part in parts[:-1]:
            tempResult = tempResult.setdefault(part, {})
        tempResult[parts[-1]] = origDict[keys]
    return result 

if __name__ == "__main__":
    
    import numarray.random_array as ra
    
    testData = 0
    if testData:
        test_data = {}
        test_data['A'] = ra.random_integers(0, 10, 5)
        test_data['B'] = ra.random_integers(10, 50, (5, 5))
        test_data['C'] = ra.random_integers(10, 50, (5, 5)) + 0j
        test_data['D'] = ra.random_integers(10, 50, (5, 5)) + 1j* \
                ra.random_integers(10, 100, (5, 5))
        test_data['E'] = ra.random_integers(10, 50, 5) + 1j*\
                ra.random_integers(10, 100, 5)
        dumpData(test_data)
        result = loadData('/home/karthik/dataloader')
        
    else:
        source, jammer = loadConfig("test.ini")
        print "--"*30 
        print "\n"
        for keys in source.keys():
            print "%s: \t %s \n"%(keys, source[keys])
        print "--"*30
        print "\n"
        for keys  in jammer.keys():
            print "%s: \t %s \n"%(keys, jammer[keys])
        print "--"*30
