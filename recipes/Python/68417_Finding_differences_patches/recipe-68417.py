#!/usr/bin/python

import os, sys, string, copy, getopt

def usage():
        print """patchdiff generates a listing of patches
that are different between two solaris boxes.

usage: patchdiff hostname1 hostname2"""

        sys.exit(1)

def getpatches(target):
        f = os.popen('/usr/local/bin/ssh ' + target + ' /bin/showrev -p', 'r')

        patch = ['', {'obsoletes': None, 'requires': None, 'incompatibles': None, 'packages': None}]
        patch_listing = []

        while 1:
                line = string.split(f.readline()[:-1])
                if not line: break # Break at EOF

                patch[0] = line[1]
                patch[1]['obsoletes'] = line[line.index('Obsoletes:')+1:line.index('Requires:')]
                patch[1]['requires'] = line[line.index('Requires:')+1:line.index('Incompatibles:')]
                patch[1]['incompatibles'] = line[line.index('Incompatibles:')+1:line.index('Packages:')]
                patch[1]['packages'] = line[line.index('Packages:')+1:]
                patch_listing.append([patch[0],copy.copy(patch[1])])

        return patch_listing

def compare(a,b):
        a_extra = []
        b_extra = []

        for i in a:
                if i not in b:
                        a_extra.append(i)
        for i in b:
                if i not in a:
                        b_extra.append(i)


        return (a_extra,b_extra)

def collapse(a):
        a.sort()
        older = []

        for i in range(0,len(a)):

                next = i+1
                try:

                        if a[i][0][0:6] == a[next][0][0:6]:
                                if a[i][0][7:9] < a[next][0][7:9]:

                                        older.append([a[i][0],copy.copy(a[i][1])])
                except: pass


        for i in older: a.remove(i)

        return a

def printout(differences):

        for i in differences[0]:
                print i[0] + "\t",
                for j in differences[1]:
                        if i[0][0:6] == j[0][0:6]:
                                print j[0],
                print ""

if len(sys.argv) != 3: usage()

options, target = getopt.getopt(sys.argv[1:], '')

patches = (collapse(getpatches(target[0])),collapse(getpatches(target[1])))

differences = compare(patches[0], patches[1])

print target[0] + '\t' + target[1]
print '---------\t---------'
printout(differences)
