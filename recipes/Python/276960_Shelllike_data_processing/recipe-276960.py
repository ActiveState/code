from itertools import izip, imap, count, ifilter
import re

def cat(fname):
    return file(fname).xreadlines()

class grep:
    """keep only lines that match the regexp"""
    def __init__(self,pat,flags=0):
        self.fun = re.compile(pat,flags).match
    def __ror__(self,input):
        return ifilter(self.fun,input)

class tr:
    """apply arbitrary transform to each sequence element"""
    def __init__(self,transform):
        self.tr=transform
    def __ror__(self,input):
        return imap(self.tr,input)

class printlines_class:
    """print sequence elements one per line"""
    def __ror__(self,input):
        for l in input:
            print l

printlines=printlines_class()

class terminator:
    """to be used at the end of a pipe-sequence"""
    def __init__(self,method):
        self.process=method
    def __ror__(self,input):
        return self.process(input)

# those objects transform generator to list, tuple or dict
aslist  = terminator(list)
asdict  = terminator(dict)
astuple = terminator(tuple)

# this object transforms seq to tuple sequence
enum = terminator( lambda input: izip(count(),input) )

#######################
# example 1: equivalent to shell grep ".*/bin/bash" /etc/passwd
cat('/etc/passwd') | tr(str.rstrip) | grep('.*/bin/bash') | printlines

#######################
# example 2: get a list of int's methods beginning with '__r'
dir(int) | grep('__r') | aslist

#######################
# example 3: useless; returns a dict {0:'l',1:'a',2:'m',3:'b',4:'d',5:'a'} 
'lambda' | enum | asdict
