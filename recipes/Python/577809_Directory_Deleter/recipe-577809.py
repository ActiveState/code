import os
from os import path
from os.path import isdir
from os.path import getsize
import shutil
from shutil import rmtree

a = raw_input("Input the directory you want to delete(Remember to give full path ex. C:\): ")
b = os.path.getsize(a)
if b == 0:
    shutil.rmtree(a)
    c = isdir(a)
    if c == False:
        print 'Your directory has been deleted.'
