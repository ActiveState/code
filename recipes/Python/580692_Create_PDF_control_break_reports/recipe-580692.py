from __future__ import print_function

# ControlBreakToPDF.py
# A program to show how to write simple control break reports
# and send the output to PDF, using itertools.groupby and xtopdf.
# Author: Vasudev Ram
# Copyright 2016 Vasudev Ram
# http://jugad2.blogspot.com
# https://gumroad.com/vasudevram

from itertools import groupby
from PDFWriter import PDFWriter

# I hard-code the data here to make the example shorter.
# More commonly, it would be fetched at run-time from a 
# database query or CSV file or similar source.

data = \
[
    ['North', 'Desktop #1', 1000],
    ['South', 'Desktop #3', 1100],
    ['North', 'Laptop #7', 1200],
    ['South', 'Keyboard #4', 200],
    ['North', 'Mouse #2', 50],
    ['East', 'Tablet #5', 200],
    ['West', 'Hard disk #8', 500],
    ['West', 'CD-ROM #6', 150],
    ['South', 'DVD Drive', 150],
    ['East', 'Offline UPS', 250],
]

pw = PDFWriter('SalesReport.pdf')
pw.setFont('Courier', 12)
pw.setHeader('Sales by Region')
pw.setFooter('Using itertools.groupby and xtopdf')

# Convenience function to both print to screen and write to PDF.
def print_and_write(s, pw):
    print(s)
    pw.writeLine(s)

# Set column headers.
headers = ['Region', 'Item', 'Sale Value']
# Set column widths.
widths = [ 10, 15, 10 ]
# Build header string for report.
header_str = ''.join([hdr.center(widths[ind]) \
    for ind, hdr in enumerate(headers)])
print_and_write(header_str, pw)

# Function to base the sorting and grouping on.
def key_func(rec):
    return rec[0]

data.sort(key=key_func)

for region, group in groupby(data, key=key_func):
    print_and_write('', pw)
    # Write group header, i.e. region name.
    print_and_write(region.center(widths[0]), pw)
    # Write group's rows, i.e. sales data for the region.
    for row in group:
        # Build formatted row string.
        row_str = ''.join(str(col).rjust(widths[ind + 1]) \
            for ind, col in enumerate(row[1:]))
        print_and_write(' ' * widths[0] + row_str, pw)
pw.close()
