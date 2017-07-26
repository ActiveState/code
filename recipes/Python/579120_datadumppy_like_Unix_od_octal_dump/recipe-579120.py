'''
Program name: data_dump.py
Version: 1
Author: Vasudev Ram.
Copyright 2015 Vasudev Ram.
Purpose: To dump the contents of a specified file or standard input, 
to the standard output, in one or more formats, such as:
    - as characters
    - as decimal numbers
    - as hexadecimal numbers
    - as octal numbers
    
Inspired by the od (octal dump) command of Unix, and intended to work,
very roughly, like it. Will not attempt to replicate od exactly or even 
closely. May diverge from od's way of doing things, as desired.
'''

# Imports:

from __future__ import print_function
import sys

# Global constants:

# Maximum number of character (from the input) to output per line.
MAX_CHARS_PER_LINE = 16

# Global variables:

# Functions:

def data_dump(infil, line_len=MAX_CHARS_PER_LINE, options=None):
    '''
    Dumps the data from the input source infil to the standard output.
    '''
    byte_addr = 0
    buf = infil.read(line_len)
    # While not EOF.
    while buf != '':
        # Print the offset of the first character to be output on this line.
        # The offset refers to the offset of that character in the input,
        # not in the output. The offset is 0-based.
        sys.stdout.write("{:>08s}: ".format(str(byte_addr)))

        # Print buf in character form, with . for control characters.
        # TODO: Change to use \n for line feed, \t for tab, etc., for 
        # those control characters which have unambiguous C escape 
        # sequences.
        byte_addr += len(buf)
        for c in buf:
            sys.stdout.write('  ') # Left padding before c as char.
            if (0 <= ord(c) <= 31) or (c == 127):
                sys.stdout.write('.')
            else:
                sys.stdout.write(c)
        sys.stdout.write('\n')

        # Now print buf in hex form.
        sys.stdout.write(' ' * 10) # Padding to match that of byte_addr above.
        for c in buf:
            sys.stdout.write(' ') # Left padding before c in hex.
            sys.stdout.write('{:>02s}'.format((hex(ord(c))[2:].upper())))
        sys.stdout.write('\n')
        buf = infil.read(line_len)
    infil.close()


def main():
    '''
    Checks the arguments, sets option flags, sets input source.
    Then calls data_dump() function with the input source and options.
    '''
    try:
        lsa = len(sys.argv)
        if lsa == 1:
            # Input from standard input.
            infil = sys.stdin
        elif lsa == 2:
            # Input from a file.
            infil = open(sys.argv[1], "rb")
        data_dump(infil)
        sys.exit(0)
    except IOError as ioe:
        print("Error: IOError: " + str(ioe))
        sys.exit(1)

if __name__ == '__main__':
    main()
