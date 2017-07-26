#!/usr/bin/python

"""
NAME

    shuffle-merge -- shuffle-merge text files

SYNOPSIS
    %(progname)s [OPTIONS] <File Name Prefix>

DESCRIPTION
    shuffle-merge merges a number of text files. The order of merging is
    selected with a random policy.
    
OPTIONS:
    Arguments:
    --help 
      Print a summary of the program options and exit.
    
    --nprocs=<int>, -n <int>
      number of processors [default=8]
    
    --maxlines=<int>, -m <int>
      max number of lines read [default=20]
      
"""

__rev = "1.0"
__author__ = 'Alexandru Iosup'
__email__ = 'A.Iosup at ewi.tudelft.nl'
__file__ = 'shuffle-merge.py'
__version__ = '$Revision: %s$' % __rev
__date__ = '$Date: 2005/08/15 16:59:00 $'
__copyright__ = 'Copyright (c) 2005 Alexandru IOSUP'
__license__ = 'Python'


import sys
import os
import getopt
import string 
import random
import time


def ShuffleMerge( InFilePrefix, NProcs, MaxLines ):
    """ 
    shuffle-merges files InFilePrefix_X, X in { 0, 1, ... NProcs } and
    stores the result into sm-InFilePrefix.
    
    Notes: does NOT check if the input files are available.
    """
    
    NProcs = int(NProcs)
    MaxLines = int(MaxLines)
    
    #-- init random seed
    random.seed(time.time())
    
    
    OutFileName = "sm-%s" % InFilePrefix
    OutFile = open( OutFileName, "w" )
    
    InFileNames = {}
    InFiles = {}
    InFileFinished = {}
    
    ProcsIDList = range(NProcs)
    
    for index in ProcsIDList:
        InFileNames[index] = "%s_%d" % (InFilePrefix, index)
        InFiles[index] = open( InFileNames[index], "r" )
        InFileFinished[index] = 0
        
    nReadLines = 0
    while 1:
        
        #-- make a list of all input files not finished yet
        ListOfNotFinished = []
        for index in ProcsIDList:
            if InFileFinished[index] == 0:
                ListOfNotFinished.append(index)
                
        #-- randomly select an input file
        lenListOfNotFinished = len(ListOfNotFinished)
        if lenListOfNotFinished == 0:
            break
        elif lenListOfNotFinished == 1:
            ProcID = ListOfNotFinished[0]
        else: 
            # at least 2 elements in this list -> pick at random the proc ID
            ProcID = ListOfNotFinished[random.randint(0, lenListOfNotFinished - 1)]
            
        #-- randomly copy 1 to MaxLines lines of it to the output file
        nLinesToGet = random.randint( 1, MaxLines )
        try:
            for index in range(nLinesToGet):
                line = InFiles[ProcID].readline()
                if len(line) > 0:
                    OutFile.write( line )
                    nReadLines = nReadLines + 1
                    if nReadLines % 10000 == 0:
                        print "nReadLines", nReadLines, "[last read", nLinesToGet, \
                              "from", ProcID, "/", ListOfNotFinished, "]"
                else:
                    InFileFinished[ProcID] = 1
        except KeyError, e:
            print "Got wrong array index:", e
        except IOError, (errno, strerror):
            print "I/O error(%s): %s" % (errno, strerror)
            InFileFinished[ProcID] = 1
        
    print "nReadLines", nReadLines, "[last read", nLinesToGet, \
                  "from", ProcID, "/", ListOfNotFinished, "]"
        
    OutFile.close()
    for index in ProcsIDList:
        InFiles[index].close()
        

def usage(progname):
    print __doc__ % vars() 


def main(argv):                  

    OneCharOpts = "hn:m:"
    MultiCharList = [
        "help", "nprocs=", "maxlines="
        ]
        
    try:                                
        opts, args = getopt.getopt( argv, OneCharOpts, MultiCharList )
    except getopt.GetoptError:
        usage(os.path.basename(sys.argv[0]))
        sys.exit(2)
    
    NProcs = 8
    MaxLines = 20
    FileNamePrefix = "ttt"
    
    for opt, arg in opts:
        if opt in ["-h", "--help"]:
            usage(os.path.basename(sys.argv[0]))
            sys.exit()
        elif opt in ["-n", "--nprocs"]: 
            NProcs = arg.strip() 
        elif opt in ["-m", "--maxlines"]: 
            MaxLines = arg.strip() 
            
    if len(args) >= 1:
        FileNamePrefix = args[0]
            
    ShuffleMerge( FileNamePrefix, NProcs, MaxLines )

if __name__ == "__main__":

    main(sys.argv[1:]) 
    
