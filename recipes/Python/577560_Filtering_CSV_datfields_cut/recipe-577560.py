#!/usr/bin/env python

"""csvcut

Tool to read and cut up CSV files by fields. Each line of the input file
is read, parsed and broken up into their respective fields. The fields
you want to extract are given by the -f/--field option by specifiying
the field number you'd like. You can specify two or more fields by
using two or more -f/--field options. Entire records/rows can be kipped
by using the -s/--skip option. If no fields are given this acts much
like the cat tool.
"""

__version__ = "0.5"
__author__ = "James Mills"

import sys
import csv
import optparse

USAGE = "%prog [options] <file>"
VERSION = "%prog v" + __version__

def parse_options():
    parser = optparse.OptionParser(usage=USAGE, version=VERSION)

    parser.add_option("-f", "--field",
            action="append", type="int",
            default=[], dest="fields",
            help="Field no. to cut (multiple allowed)")

    parser.add_option("-s", "--skip",
            action="append", type="int",
            default=[], dest="skip",
            help="Specify records to skip (multiple allowed)")

    opts, args = parser.parse_args()

    if len(args) < 1:
        parser.print_help()
        raise SystemExit, 1

    return opts, args

def generate_rows(f):
    sniffer = csv.Sniffer()
    dialect = sniffer.sniff(f.readline())
    f.seek(0)

    reader = csv.reader(f, dialect)
    for line in reader:
        yield line

def main():
    opts, args = parse_options()

    filename = args[0]

    if filename == "-":
        fd = sys.stdin
    else:
        fd = open(filename, "rU")

    rows = generate_rows(fd)

    for i, row in enumerate(rows):
        if i in opts.skip:
            continue

        if opts.fields:
            print ",".join([row[x] for x in opts.fields])
        else:
            print ",".join(row)

if __name__ == "__main__":
    main()
