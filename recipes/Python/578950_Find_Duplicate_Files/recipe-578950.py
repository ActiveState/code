# Find Duplicate Files
# FB36 - 20141012
import sys
import os
import glob
import hashlib

numArgs = len(sys.argv) # of command-line arguments
if numArgs < 2 or numArgs > 3:
    print "USAGE:"
    print "[python] FindDuplicateFiles.py FilePath [FilePath2]"
    print "FilePath2 is optional."
    print "If file path(s) have spaces then add quotes around."
    print "File path(s) must include wildcards in the end"
    print "like ...\*.*"
    os._exit(1)
if numArgs > 1:
    filePath1 = sys.argv[1]
    filePath2 = filePath1
if numArgs > 2:
    filePath2 = sys.argv[2]

fileList1 = glob.glob(filePath1)
fileList2 = glob.glob(filePath2)

fileSizeList1 = []
for fn1 in fileList1:
    fileSizeList1.append(os.path.getsize(fn1))

fileSizeList2 = []
for fn2 in fileList2:
    fileSizeList2.append(os.path.getsize(fn2))

# Find groups of files which have same size
fileSizeGroups = dict()
for i in range(len(fileList1)):
    if fileSizeList1[i] not in fileSizeGroups:
        fileSizeGroups[fileSizeList1[i]] = [fileList1[i]]
    elif fileList1[i] not in fileSizeGroups[fileSizeList1[i]]:
        fileSizeGroups[fileSizeList1[i]].append(fileList1[i])

for i in range(len(fileList2)):
    if fileSizeList2[i] not in fileSizeGroups:
        fileSizeGroups[fileSizeList2[i]] = [fileList2[i]]
    elif fileList2[i] not in fileSizeGroups[fileSizeList2[i]]:
        fileSizeGroups[fileSizeList2[i]].append(fileList2[i])
    
# Find groups of files which have same size and same hash
fileHashGroups = dict()
for fileSize in fileSizeGroups.keys():
    if len(fileSizeGroups[fileSize]) > 1:
        for fn in fileSizeGroups[fileSize]:
            fileHash = hashlib.sha256(open(fn, 'rb').read()).hexdigest()
            if fileHash not in fileHashGroups:
                fileHashGroups[fileHash] = [fn]
            elif fn not in fileHashGroups[fileHash]:
                fileHashGroups[fileHash].append(fn)

# Output groups of files which have same size and same hash
for fileHash in fileHashGroups.keys():
    if len(fileHashGroups[fileHash]) > 1:
        for fn in fileHashGroups[fileHash]:
            print fn
        print
