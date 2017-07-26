#version 0
import sys

f1 = open(sys.argv[1], "r")
f2 = open(sys.argv[2], "r")

fileOne = f1.readlines()
fileTwo = f2.readlines()

f1.close()
f2.close()

outFile1 = open(sys.argv[3], "w")
outFile2 = open(sys.argv[4], "w")

for i in fileOne:
        if not i in fileTwo:
                outFile1.write(i)

for i in fileTwo:
        if not i in fileOne:
                outFile2.write(i)

outFile1.close()
outFile2.close()

#first time refacotring 
import sys
from operator import attrgetter,itemgetter

#verify inputs
USAGE='''
%s file1 file2 output1 output2
'''% __file__

if len(sys.argv)<5:
        print USAGE
        sys.exit(2)

#open files with try
try:
        f1 = open(sys.argv[1], "r")
        f2 = open(sys.argv[2], "r")
except Exception,e:
        print 'encounter issues %s, while opening in files: %s %s' % (str(e),itemgetter(1)(sys.argv),itemgetter(2)(sys.argv))
        sys.exit(1)

fileOne = f1.readlines()
fileTwo = f2.readlines()

f1.close()
f2.close()

#open files with try
try:
        outFile1 = open(sys.argv[3], "w")
        outFile2 = open(sys.argv[4], "w")
except Exception,e:
        print 'encounter issues %s, while opening out files: %s %s' % (str(e),itemgetter(3)(sys.argv),itemgetter(4)(sys.argv))
        sys.exit(1)

l_minus=lambda x,y:list(set(x)-set(y))

outFile1.write('\n'.join(l_minus(fileOne,fileTwo)))
outFile2.write('\n'.join(l_minus(fileTwo,fileOne)))

outFile1.close()
outFile2.close()


#2nd time refactoring
import sys
from operator import attrgetter,itemgetter

#verify inputs
USAGE='''
%s file1 file2 output1 output2
'''% __file__

if len(sys.argv)<5:
        print USAGE
        sys.exit(2)

#open files with try
with open(itemgetter(1)(sys.argv), "r") as f1, open(itemgetter(2)(sys.argv), "r") as f2:
        fileOne = f1.readlines()
        fileTwo = f2.readlines()

#list subset
l_minus=lambda x,y:list(set(x)-set(y))
#open files with try
with open(itemgetter(3)(sys.argv), "w") as outFile1, open(itemgetter(4)(sys.argv), "w") as outFile2:
        outFile1.write('\n'.join(l_minus(fileOne,fileTwo)))
        outFile2.write('\n'.join(l_minus(fileTwo,fileOne)))
