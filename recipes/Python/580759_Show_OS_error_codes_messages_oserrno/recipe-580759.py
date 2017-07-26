from __future__ import print_function
'''
os_errno_info.py
To show the error codes and 
names from the os.errno module.
Author: Vasudev Ram
Copyright 2017 Vasudev Ram
Web site: https://vasudevram.github.io
Blog: https://jugad2.blogspot.com
Product store: https://gumroad.com/vasudevram
'''

import sys
import os

def main():
    
    print("Showing error codes and names\nfrom the os.errno module:")
    print("Python sys.version:", sys.version[:6])
    print("Number of error codes:", len(os.errno.errorcode))
    print("{0:>4}{1:>8}   {2:<20}    {3:<}".format(\
        "Idx", "Code", "Name", "Message"))
    for idx, key in enumerate(sorted(os.errno.errorcode)):
        print("{0:>4}{1:>8}   {2:<20}    {3:<}".format(\
            idx, key, os.errno.errorcode[key], os.strerror(key)))

if __name__ == '__main__':
    main()

Output of run
