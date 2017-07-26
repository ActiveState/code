from __future__ import print_function
'''
file_glob.py
Lists filenames matching one or more wildcard patterns.
Author: Vasudev Ram
Copyright 2016 Vasudev Ram
Web site: https://vasudevram.github.io
Blog: http://jugad2.blogspot.com
Product store: https://gumroad.com/vasudevram
'''

import sys
import glob

sa = sys.argv
lsa = len(sys.argv)

if lsa < 2:
    print("{}: Must give one or more filename wildcard arguments.".
        format(sa[0]))
    sys.exit(1)

for arg in sa[1:]:
    print("Files matching pattern {}:".format(arg))
    for filename in glob.glob(arg):
            print(filename)
