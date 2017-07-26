#! /usr/bin/python

import os
import sys
import stat
import md5

filesBySize = {}

def walker(arg, dirname, fnames):
    d = os.getcwd()
    os.chdir(dirname)
    try:
        fnames.remove('Thumbs')
    except ValueError:
        pass        
    for f in fnames:
        if not os.path.isfile(f):
            continue
        size = os.stat(f)[stat.ST_SIZE]
        if size < 100:
            continue
        if filesBySize.has_key(size):
            a = filesBySize[size]
        else:
            a = []
            filesBySize[size] = a
        a.append(os.path.join(dirname, f))
    os.chdir(d)

for x in sys.argv[1:]:
    print 'Scanning directory "%s"....' % x
    os.path.walk(x, walker, filesBySize)    

print 'Finding potential dupes...'
potentialDupes = []
potentialCount = 0
trueType = type(True)
sizes = filesBySize.keys()
sizes.sort()
for k in sizes:
    inFiles = filesBySize[k]
    outFiles = []
    hashes = {}
    if len(inFiles) is 1: continue
    print 'Testing %d files of size %d...' % (len(inFiles), k)
    for fileName in inFiles:
        if not os.path.isfile(fileName):
            continue
        aFile = file(fileName, 'r')
        hasher = md5.new(aFile.read(1024))
        hashValue = hasher.digest()
        if hashes.has_key(hashValue):
            x = hashes[hashValue]
            if type(x) is not trueType:
                outFiles.append(hashes[hashValue])
                hashes[hashValue] = True
            outFiles.append(fileName)
        else:
            hashes[hashValue] = fileName
        aFile.close()
    if len(outFiles):
        potentialDupes.append(outFiles)
        potentialCount = potentialCount + len(outFiles)
del filesBySize

print 'Found %d sets of potential dupes...' % potentialCount
print 'Scanning for real dupes...'

dupes = []
for aSet in potentialDupes:
    outFiles = []
    hashes = {}
    for fileName in aSet:
        print 'Scanning file "%s"...' % fileName
        aFile = file(fileName, 'r')
        hasher = md5.new()
        while True:
            r = aFile.read(4096)
            if not len(r):
                break
            hasher.update(r)
        aFile.close()
        hashValue = hasher.digest()
        if hashes.has_key(hashValue):
            if not len(outFiles):
                outFiles.append(hashes[hashValue])
            outFiles.append(fileName)
        else:
            hashes[hashValue] = fileName
    if len(outFiles):
        dupes.append(outFiles)

i = 0
for d in dupes:
    print 'Original is %s' % d[0]
    for f in d[1:]:
        i = i + 1
        print 'Deleting %s' % f
        os.remove(f)
    print
