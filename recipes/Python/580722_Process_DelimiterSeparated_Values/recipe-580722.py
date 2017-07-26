from __future__ import print_function

"""
read_dsv.py
Author: Vasudev Ram
Web site: https://vasudevram.github.io
Blog: https://jugad2.blogspot.com
Product store: https://gumroad.com/vasudevram
Purpose: Shows how to read DSV data, i.e. 

https://en.wikipedia.org/wiki/Delimiter-separated_values 

from either files or standard input, split the fields of each
line on the delimiter, and process the fields in some way.
The delimiter character is configurable by the user and can
be specified as either a character or its ASCII code.

Reference:
TAOUP (The Art Of Unix Programming): Data File Metaformats:
http://www.catb.org/esr/writings/taoup/html/ch05s02.html
ASCII table: http://www.asciitable.com/
"""

import sys
import string

def err_write(message):
    sys.stderr.write(message)

def error_exit(message):
    err_write(message)
    sys.exit(1)

def usage(argv, verbose=False):
    usage1 = \
        "{}: read and process DSV (Delimiter-Separated-Values) data.\n".format(argv[0])
    usage2 = "Usage: python" + \
        " {} [ -c delim_char | -n delim_code ] [ dsv_file ] ...\n".format(argv[0])
    usage3 = [
        "where one of either the -c or -n option must be given,\n",  
        "delim_char is a single ASCII delimiter character, and\n", 
        "delim_code is a delimiter character's ASCII code.\n", 
        "Text lines will be read from specified DSV file(s) or\n", 
        "from standard input, split on the specified delimiter\n", 
        "specified by either the -c or -n option, processed, and\n", 
        "written to standard output.\n", 
    ]
    err_write(usage1)
    err_write(usage2)
    if verbose:
        for line in usage3:
            err_write(line)

def str_to_int(s):
    try:
        return int(s)
    except ValueError as ve:
        error_exit(repr(ve))

def valid_delimiter(delim_code):
    return not invalid_delimiter(delim_code)

def invalid_delimiter(delim_code):
    # Non-ASCII codes not allowed, i.e. codes outside
    # the range 0 to 255.
    if delim_code < 0 or delim_code > 255:
        return True
    # Also, don't allow some specific ASCII codes;
    # add more, if it turns out they are needed.
    if delim_code in (10, 13):
        return True
    return False

def read_dsv(dsv_fil, delim_char):
    for idx, lin in enumerate(dsv_fil):
        fields = lin.split(delim_char)
        assert len(fields) > 0
        # Knock off the newline at the end of the last field,
        # since it is the line terminator, not part of the field.
        if fields[-1][-1] == '\n':
            fields[-1] = fields[-1][:-1]
        # Treat a blank line as a line with one field,
        # an empty string (that is what split returns).
        print("Line", idx, "fields:")
        for idx2, field in enumerate(fields):
            print(str(idx2) + ":", "|" + field + "|")

def main():
    # Get and check validity of arguments.
    sa = sys.argv
    lsa = len(sa)
    if lsa == 1:
        usage(sa)
        sys.exit(0)
    if lsa == 2:
        # Allow the help option with any letter case.
        if sa[1].lower() in ("-h", "--help"):
            usage(sa, verbose=True)
            sys.exit(0)
        else:
            usage(sa)
            sys.exit(0)

    # If we reach here, lsa is >= 3.
    # Check for valid mandatory options (sic).
    if not sa[1] in ("-c", "-n"):
        usage(sa, verbose=True)
        sys.exit(0)

    # If -c option given ...
    if sa[1] == "-c":
        # If next token is not a single character ...
        if len(sa[2]) != 1:
            error_exit(
            "{}: Error: -c option needs a single character after it.".format(sa[0]))
        if not sa[2] in string.printable:
            error_exit(
            "{}: Error: -c option needs a printable ASCII character after it.".format(\
            sa[0]))
        delim_char = sa[2]
    # else if -n option given ...
    elif sa[1] == "-n":
        delim_code = str_to_int(sa[2])
        if invalid_delimiter(delim_code):
            error_exit(
            "{}: Error: invalid delimiter code {} given for -n option.".format(\
            sa[0], delim_code))
        delim_char = chr(delim_code)
    else:
        # Checking for what should not happen ... a bit of defensive programming here.
        error_exit("{}: Program error: neither -c nor -n option given.".format(sa[0]))

    try:
        # If no filenames given, read sys.stdin ...
        if lsa == 3:
            print("processing sys.stdin")
            dsv_fil = sys.stdin
            read_dsv(dsv_fil, delim_char)
            dsv_fil.close()
        # else (filenames given), read them ...
        else:
            for dsv_filename in sa[3:]:
                print("processing file:", dsv_filename)
                dsv_fil = open(dsv_filename, 'r')
                read_dsv(dsv_fil, delim_char)
                dsv_fil.close()
    except IOError as ioe:
        error_exit("{}: Error: {}".format(sa[0], repr(ioe)))
        
if __name__ == '__main__':
    main()
