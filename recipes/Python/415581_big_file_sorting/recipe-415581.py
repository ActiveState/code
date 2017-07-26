import os

class FileSort(object):
    def __init__(self, inFile, outFile=None, splitSize=20):
        """ split size (in MB) """
        self._inFile = inFile
        if outFile is None:
            self._outFile = inFile
        else:
            self._outFile = outFile
                    
        self._splitSize = splitSize * 1000000
        self.setKeyExtractMethod()

        
    def setKeyExtractMethod(self, keyExtractMethod=None):
        """ key extract from line for sort method:
            def f(line):
                return line[1:3], line[5:10]
        """                
        if keyExtractMethod is None:
            self._getKey = lambda line: line
        else:
            self._getKey = keyExtractMethod

    def sort(self):
        files = self._splitFile()

        if files is None:
            """ file size <= self._splitSize """            
            self._sortFile(self._inFile, self._outFile)
            return

        for fn in files:
            self._sortFile(fn)
            
        self._mergeFiles(files)
        self._deleteFiles(files)

        
    def _sortFile(self, fileName, outFile=None):
        lines = open(fileName).readlines()
        get_key = self._getKey
        data = [(get_key(line), line) for line in lines if line!='']
        data.sort()
        lines = [line[1] for line in data]        
        if outFile is not None:
            open(outFile, 'w').write(''.join(lines))
        else:
            open(fileName, 'w').write(''.join(lines))
    
    

    def _splitFile(self):
        totalSize = os.path.getsize(self._inFile)
        if totalSize <= self._splitSize:
            # do not split file, the file isn't so big.
            return None

        fileNames = []            
                
        fn,e = os.path.splitext(self._inFile)
        f = open(self._inFile)
        try:
            i = size = 0
            lines = []
            for line in f:
                size += len(line)
                lines.append(line)
                if size >= self._splitSize:
                    i += 1
                    tmpFile = fn + '.%03d' % i
                    fileNames.append(tmpFile)
                    open(tmpFile,'w').write(''.join(lines))
                    del lines[:]
                    size = 0

                                                       
            if size > 0:
                tmpFile = fn + '.%03d' % (i+1)
                fileNames.append(tmpFile)
                open(tmpFile,'w').write(''.join(lines))
                
            return fileNames
        finally:
            f.close()

    def _mergeFiles(self, files):
        files = [open(f) for f in files]
        lines = []
        keys = []
        
        for f in files:
            l = f.readline()        
            lines.append(l)
            keys.append(self._getKey(l))

        buff = []
        buffSize = self._splitSize/2
        append = buff.append
        output = open(self._outFile,'w')
        try:
            key = min(keys)
            index = keys.index(key)
            get_key = self._getKey
            while 1:
                while key == min(keys):
                    append(lines[index])
                    if len(buff) > buffSize:
                        output.write(''.join(buff))
                        del buff[:]
                            
                    line = files[index].readline()
                    if not line:
                        files[index].close()
                        del files[index]
                        del keys[index]
                        del lines[index]
                        break
                    key = get_key(line)
                    keys[index] = key
                    lines[index] = line
        
                if len(files)==0:
                    break
                # key != min(keys), see for new index (file)
                key = min(keys)
                index = keys.index(key)

            if len(buff)>0:
                output.write(''.join(buff))
        finally:    
            output.close()

    def _deleteFiles(self, files):   
        for fn in files:
            os.remove(fn)        
        

            
def sort(inFileName, outFileName=None, getKeyMethod=None):
    fs = FileSort(inFileName, outFileName)
    if getKeyMethod is not None:
        fs.setKeyExtractMethod(getKeyMethod)

    fs.sort()
    fs = None
