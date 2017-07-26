# -*- coding: Windows-1251 -*-
'''
rename_to_exiftime.py

Rename JPEG files according to EXIF-date using PIL

If global variable CREATE_HARDLINK is set, script creates Windows (XP) batch file 
for creating hardlink version of source files

Author: Denis Barmenkov <denis.barmenkov@gmail.com>

Modified by: Jorge Barnaby <jorge.barnaby@gmail.com>
Improved rename process on duplicates

Copyright: this code is free, but if you want to use it, 
           please keep this multiline comment along with function source. 
           Thank you.

2009-02-10 18:14 
'''

import Image

import os
import re
import sys
import time

CREATE_HARDLINK=0

def extract_jpeg_exif_time(jpegfn):
    if not os.path.isfile(jpegfn):
        return None
    try:
        im = Image.open(jpegfn)
        if hasattr(im, '_getexif'):
            exifdata = im._getexif()
            ctime = exifdata[0x9003]
            #print ctime
            return ctime
    except: 
        _type, value, traceback = sys.exc_info()
        print "Error:\n%r", value
    
    return None

def get_exif_prefix(jpegfn):
    ctime = extract_jpeg_exif_time(jpegfn)
    if ctime is None:
        return None
    ctime = ctime.replace(':', '')
    ctime = re.sub('[^\d]+', '_', ctime)
    return ctime

def rename_jpeg_file(fn):
    if not os.path.isfile(fn):
        return 0
    ext = os.path.splitext(fn)[1].lower()
    if ext not in ['.jpg', '.jpeg', '.jfif', '.nef', '.png']:
        return 0
    path, base = os.path.split(fn)
    #print base # status
    prefix = get_exif_prefix(fn)
    if prefix is None:
        print '%s could not be renamed' % (base)
        return 0
    if base.startswith(prefix):
        print '%s file already renamed' % (base)
        return 0 # file already renamed to this prefix
    
    exists = True
    index = 0
    while exists:
        if index == 0:
            new_name = prefix + ext # + '_' + base
        else:
            new_name = prefix + '_' + str(index) + ext
        new_full_name = os.path.join(path, new_name)
        exists = os.path.isfile(new_full_name)
        index = index + 1

    if CREATE_HARDLINK:
        f = open('CREATE_HARDLINK.cmd', 'a')
        f.write('fsutil hardlink create "%s" "%s"\n' % (new_full_name, fn))
        f.close()
    else:
        try:
            os.rename(fn, new_full_name)
            print '%s renamed to %s' % (base, new_name) 
        except:
            print 'ERROR rename %s --> %s' % (fn, new_full_name)
            return 0

    return 1

def rename_jpeg_files_in_dir(dn):
    names = os.listdir(dn)
    count=0
    for n in names:
        file_path = os.path.join(dn, n)
        count += rename_jpeg_file(file_path)
    return count


if __name__=='__main__':
    try:
        path = sys.argv[1]
    except IndexError:
        print '''Usage:  

  rename_to_exiftime.py  filename.[jpeg|jpg|jfif]

or

  rename_to_exiftime.py  dirname
'''
        sys.exit(1)

    if os.path.isfile(path):
        rename_jpeg_file(path)
    elif os.path.isdir(path):
        count = rename_jpeg_files_in_dir(path)
        print '%d file(s) renamed.' % count
    else:
        print 'ERROR: path not found: %s' % path
