import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("file1", help="First file whose lines you want to check")
parser.add_argument("file2", help="Second file, in which you want to search for lines from first file")
args = parser.parse_args()

file1 = open(args.file1)
file2 = open(args.file2)

print "Comparing:"
print args.file1
print "and"
print args.file2
print ""
print "Attempting to find lines in *file1* that are missing in *file2*"
print ""
file1array = file1.readlines()
file2a = file2.readlines()
lengthfile1array = len(file1array)
j=0;
for file1item in file1array:
    j += 1
    sys.stdout.write("Checking line#: %d/" %(j))
    sys.stdout.write("%d   \r" %(lengthfile1array))
    i=0;
    for file2item in file2a:
        if file1item.rstrip() == file2item.rstrip():
            i += 1
            break
        else:
            i += 1
        
        if i == len(file2a):
            print "MISSING LINE FOUND at Line# " + str(j)
