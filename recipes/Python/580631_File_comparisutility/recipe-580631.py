# file_compare.py
# A simple file comparison utility.
# Author: Vasudev Ram
# Copyright 2016 Vasudev Ram

import sys
import os
from os.path import exists, getsize

def out_write(msg):
    sys.stdout.write(msg)

def err_write(msg):
    sys.stderr.write(msg)

def usage():
    err_write("Usage: {} file_a file_b\n".format(sys.argv[0]))

def file_object_compare(in_fil_a, in_fil_b):
    '''Logic: Assume files are equal to start with.
    Read both files, character by character.
    Compare characters at corresponding byte offsets. 
    If any pair at the same offset don't match, the files 
    are unequal. If we reach the end of the files, and 
    there was no mismatch, the files are equal.  We do not
    check for one file being a strict subset of the other, 
    because we only enter this function if the files are 
    of the same size.'''

    files_are_equal = True
    pos = 0
    while True:
        ca = in_fil_a.read(1)
        if ca == '':
            break
        cb = in_fil_b.read(1)
        if cb == '':
            break
        if ca != cb:
            files_are_equal = False
            break
        pos += 1
        if pos % 10000 == 0:
            print pos, 

    if files_are_equal:
        return (True, None)
    else:
        return (False, "files differ at byte offset {}".format(pos))

def file_compare(in_filename_a, in_filename_b):
    '''Compare the files in_filename_a and in_filename_b.
    If their contents are the same, return (True, None).
    else return (False, "[reason]"), where [reason] 
    is the reason why they are different, as a string.
    Reasons could be: file sizes differ or file contents differ.'''

    if getsize(in_filename_a) != getsize(in_filename_b):
        return (False, "file sizes differ")
    else:
        in_fil_a = open(in_filename_a, "rb")
        in_fil_b = open(in_filename_b, "rb")
        result = file_object_compare(in_fil_a, in_fil_b)
        in_fil_a.close()
        in_fil_b.close()
        return result
        
def main():
    if len(sys.argv) != 3:
        usage()
        sys.exit(1)

    try:
        # Get the input filenames.
        in_filename_a, in_filename_b = sys.argv[1:3]
        # Check they exist.
        for in_filename in (in_filename_a, in_filename_b):
            if not exists(in_filename):
                err_write(
                    "Error: Input file '{}' not found.\n".format(in_filename))
                sys.exit(1)
        # Don't allow comparing a file with itself.
        if in_filename_a == in_filename_b:
            out_write("No sense comparing {} against itself.".format(in_filename_a))
            sys.exit(0)
        # Compare the files.
        result = file_compare(in_filename_a, in_filename_b)
        if result[0]:
            out_write("Files compare equal.")
        else:
            out_write("Files compare unequal: {}".format(result[1]))
        sys.exit(0)
    except IOError as ioe:
        sys.stderr.write("Caught IOError: {}\n".format(str(ioe)))
    except Exception as e:
        sys.stderr.write("Caught Exception: {}\n".format(str(e)))

if __name__ == '__main__':
    main()
