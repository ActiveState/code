#!/usr/bin/env python
# convert unicode filenames to pure ascii

import os
import sys
import glob
import unicodedata 

EXT = u'*.*'

def remove_accents(s): 
    nkfd_form = unicodedata.normalize('NFKD', s) 
    return u''.join([c for c in nkfd_form if not unicodedata.combining(c)])

for fname in glob.glob(EXT):
    new_fname = remove_accents(fname)
    if new_fname != fname:
        try:
            print 'renaming non-ascii filename to', new_fname
            os.rename(fname, new_fname)
        except Exception as e:
            print e
