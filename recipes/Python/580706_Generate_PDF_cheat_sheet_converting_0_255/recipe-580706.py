# number_systems.py:

from __future__ import print_function
from PDFWriter import PDFWriter
import sys

'''
A program to generate a table of numbers from 
0 to 255, in 4 numbering systems:
    - binary
    - octal
    - decimal
    - hexadecimal
Author: Vasudev Ram
Copyright 2016 Vasudev Ram
Web site: https://vasudevram.github.io
Blog: http://jugad2.blogspot.com
Product store on Gumroad: https://gumroad.com/vasudevram
'''

def print_and_write(s, pw):
    print(s)
    pw.writeLine(s)

sa, lsa = sys.argv, len(sys.argv)
if lsa == 1:
    sys.stderr.write("Usage: {} out_filename.pdf\n".format(sa[0]))
    sys.exit(1)

with PDFWriter(sa[1]) as pw:

    pw.setFont('Courier', 12)
    pw.setHeader('*** Number table: 0 to 255 in bases 2, 8, 10, 16 ***')
    pw.setFooter('*** By xtopdf: https://google.com/search?q=xtopdf ***')
    b = "Bin"; o = "Oct"; d = "Dec"; h = "Hex"
    header = "{b:>10}{o:>10}{d:>10}{h:>10}".format(b=b, o=o, d=d, h=h)

    for i in range(256):
        if i % 16 == 0:
            print_and_write(header, pw)
        print_and_write("{b:>10}{o:>10}{d:>10}{h:>10}".format( \
            b=bin(i), o=oct(i), d=str(i), h=hex(i)), pw)

    print_and_write(header, pw)
