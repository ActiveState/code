#!/usr/bin/env python
"""

A convenience script to update a pre-specified folder containing 
subversion, mercurial, bazaar, and/or git source folders

To use it: 
    
    - change the 'src' variable below to point to your source folder

    - name this script to something appropriate (I call it 'update')
    
    - put it into a directory on your PATH


"""

import os, sys

# define source folder here
src = '/home/user/src'

def run(cmd):
    print cmd
    os.system(cmd)

operations = {
    '.bzr': ['bzr pull', 'bzr update'],
    '.hg': ['hg pull', 'hg update'],
    '.svn': ['svn update'],
    '.git': ['git pull']
} 

for folder in os.listdir(src):
    target = os.path.join(src, folder)
    if os.path.isdir(target):
        contents = os.listdir(target)
        for f in contents:
            if f in operations:
                print
                # print f, target
                os.chdir(target)
                cmds = operations[f]
                print
                print target, '-->',
                for cmd in cmds:
                    run(cmd)
