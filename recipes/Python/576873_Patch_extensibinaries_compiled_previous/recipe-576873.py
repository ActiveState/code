# -*- coding: Windows-1251 -*-
'''
find_dll_name.py

List all python dll names in DLL/PYD/etc file.

Author: Denis Barmenkov <denis.barmenkov@gmail.com>

Copyright: this code is free, but if you want to use it, 
           please keep this multiline comment along with source. 
           Thank you.

2009-08-09
'''
import re
import sys

fn = sys.argv[1]
f = open(fn, 'rb')
data = f.read()
f.close()

dll_re = re.compile(r'python\d\d\.dll', re.M | re.S)

found = dll_re.findall(data)

print found

#-------------- cut here -----------------#

# -*- coding: Windows-1251 -*-
'''
patch_dll_name.py

Patch extension precompiled binary by changing python dll name.

Author: Denis Barmenkov <denis.barmenkov@gmail.com>

Copyright: this code is free, but if you want to use it, 
           please keep this multiline comment along with source. 
           Thank you.

2009-08-09
'''

import sys
import os

OLD_NAME = 'python23.dll'
NEW_NAME = 'python24.dll'

fn = sys.argv[1]
f = open(fn, 'rb')
data = f.read()
f.close()

data = data.replace(OLD_NAME, NEW_NAME)

bak_fn = fn + '.bak'
os.rename(fn, bak_fn) # rename original file to .BAK

f = open(fn, 'wb')
f.write(data) # write patched version
f.close()
