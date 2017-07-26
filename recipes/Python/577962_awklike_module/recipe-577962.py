"""
Awk like module

Usage:

    for al in awk_iter_open("some filename"):
        print al._nr   # AWK NR
        print al._nf   # AWK NF
        print al._0r  # AWK $0
        print al._1   # AWK strip($1)
        print al._1r  # AWK $1 , raw string
        print al._1i  # AWK int($1)
        print al._1f  # AWK float($1)
"""

import re
def match(s, pattern):
    return re.match(pattern, s)

class AwkLine(object):
    def __init__(self, line, linenumber=0, sep = None, *args, **kw):
        self.line = line.rstrip()
        self.fields = line.split(sep)
        self.nr = linenumber
        super(AwkLine, self).__init__(*args, **kw)
    
    def __getattr__(self, name):
        if name in ["nr,", "_nr", "linenumber"]:
            return self.nr
            
        if name in [ "_nf", "_n", "n", "nf"]:
            return len(self.fields)
            
        if not name.startswith("_"):
            raise AttributeError  
            
        if name == "_0":
            return self.line.strip()
        if name == "_0r":
            return self.line
        
        if name.endswith("i"):
            return int(self.__getattr__(name[:-1]))
        if name.endswith("f"):
            return float(self.__getattr__(name[:-1]))
        if name.endswith("r"): #1r, 2r, 3r
            try:
                index = int(name[1:-1])
                return self.fields[index-1]
            except:
                raise AttributeError
        else: # 1, 2, 3
            try:
                index = int(name[1:])
                return self.fields[index-1].strip()
            except:
                raise AttributeError

def awk_iter(thefile, sep = None):
    for i, line in enumerate(thefile):
        yield AwkLine(line, i, sep)

def awk_iter_open(filename, sep=None):
    thefile = open(filename, "rt")
    for i, line in enumerate(thefile):
        yield AwkLine(line, i, sep)
    thefile.close()
#
if __name__ == "__main__":
    x =  AwkLine("hello, this is a test for int 100 and float 3.3") 
    print x._nr
    print x._nf
    print x._0
    print x._1
    print x._8i
    print x._11f
    for al in awk_iter_open("awk.py"): # this file itself
        print al.nr, al._0r
