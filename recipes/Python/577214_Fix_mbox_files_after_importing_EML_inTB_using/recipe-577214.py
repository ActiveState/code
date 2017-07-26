# -*- coding: Windows-1251 -*-
'''
fix_mbox_from.py

  Utility for fixing incorrect 'From' line after batch .EML files import 
  via Thunderbird's ImportExportTools version LE 2.3.2.1.

  2010-05-01 bug report sent to addon author.

  
mailbox.py (Python 2.4.5) pattern for matching 'From' line:

    _fromlinepattern = r"From \s*[^\s]+\s+\w\w\w\s+\w\w\w\s+\d?\d\s+" \
                       r"\d?\d:\d\d(:\d\d)?(\s+[^\s]+)?\s+\d\d\d\d\s*$"

Correct 'From':
From - Tue Apr 27 19:42:22 2010

Broken 'From':
From - Sat May 01 2010 15:07:31 GMT+0400 (Russian Daylight Time)
'''
import sys
import re
import os

__author__ = 'Denis Barmenkov <denis.barmenkov@gmail.com>'
__source__ = 'http://code.activestate.com/recipes/577214-fix-mbox-files-after-importing-eml-into-tb-using-i/'

bad_pattern_text = r"^(From \s*[^\s]+\s+\w\w\w\s+\w\w\w\s+\d?\d)\s+" \
                   r"(\d\d\d\d)\s+(\d?\d:\d\d(:\d\d)?)\s+" \
                   r"GMT\+\d\d\d\d\s+\([^\)]+\)\s*$"

bad_pattern = re.compile(bad_pattern_text)

mbox_fn = sys.argv[1]
print 'File: %s' % mbox_fn
temp_fn = mbox_fn + '.temp'
orig_fn = mbox_fn + '.source'
assert not os.path.exists(orig_fn)

#src_size = os.path.getsize(mbox_fn)

fsrc = open(mbox_fn, 'r')
fdest = open(temp_fn, 'w')

fix_count = 0
for line_index, rawline in enumerate(fsrc):
    #if line_index % 100 == 0:
    #    pos = fsrc.tell()
    #    print '%d%%,' % (100 * pos // src_size),
    line = rawline.splitlines()[0]
    m = bad_pattern.match(line)
    if m:
        line = '%s %s %s' % m.group(1, 3, 2)
        fix_count += 1
    fdest.write(line + '\n')
print 
print 'Fixed %s "From" lines' % fix_count

fdest.close()
fsrc.close()

os.rename(mbox_fn, orig_fn)
os.rename(temp_fn, mbox_fn)
