#!/usr/bin/env python

"""csv2sql

Tool to convert CSV data files into SQL statements that
can be used to populate SQL tables. Each line of text in
the file is read, parsed and converted to SQL and output
to stdout (which can be piped).

A table to populate is given by the -t/--table option or
by the basename of the input file (if not standard input).

Fields are either given by the -f/--fields option (comma
separated) or determinted from the first row of data.
"""

__version__ = "0.4"
__author__ = "James Mills"
__date__ = "3rd February 2011"

import os
import csv
import sys
import optparse

USAGE = "%prog [options] <file>"
VERSION = "%prog v" + __version__

def parse_options():
    parser = optparse.OptionParser(usage=USAGE, version=VERSION)

    parser.add_option("-t", "--table",
            action="store", type="string",
            default=None, dest="table",
            help="Specify table name (defaults to filename)")

    parser.add_option("-f", "--fields",
            action="store", type="string",
            default=None, dest="fields",
            help="Specify a list of fields (comma-separated)")

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
        if opts.table is None:
            print "ERROR: No table specified and stdin used."
            raise SystemExit, 1
        fd = sys.stdin
        table = opts.table
    else:
        fd = open(filename, "rU")
        if opts.table is None:
            table = os.path.splitext(filename)[0]
        else:
            table = opts.table

    rows = generate_rows(fd)

    if opts.fields:
        fields = ", ".join([x.strip() for x in opts.fields.split(",")])
    else:
        fields = ", ".join(rows.next())

    for i, row in enumerate(rows):
        if i in opts.skip:
            continue

        values = ", ".join(["\"%s\"" % x for x in row])
        print "INSERT INTO %s (%s) VALUES (%s);" % (table, fields, values)

if __name__ == "__main__":
    main()
