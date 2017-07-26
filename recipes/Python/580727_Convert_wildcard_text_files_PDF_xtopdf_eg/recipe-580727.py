from __future__ import print_function

# WildcardTextToPDF.py
# Convert the text files specified by a filename wildcard,
# like '*.txt' or 'foo*bar*baz.txt', to PDF files.
# Each text file's content goes to a separate PDF file, with the 
# PDF file name being the full text file name (including the 
# '.txt' part), with '.pdf' appended.
# Requires:
# - xtopdf: https://bitbucket.org/vasudevram/xtopdf
# - ReportLab: https://www.reportlab.com/ftp/reportlab-1.21.1.tar.gz
# Author: Vasudev Ram
# Copyright 2016 Vasudev Ram
# Product store: https://gumroad.com/vasudevram
# Web site: https://vasudevram.github.io
# Blog: http://jugad2.blogspot.com

import sys
import glob
from PDFWriter import PDFWriter

def usage(argv):
    sys.stderr.write("Usage: python {} txt_filename_pattern\n".format(argv[0]))
    sys.stderr.write("E.g. python {} foo*.txt\n".format(argv[0]))

def text_to_pdf(txt_filename):
    pw = PDFWriter(txt_filename + '.pdf')
    pw.setFont('Courier', 12)
    pw.setHeader('{} converted to PDF'.format(txt_filename))
    pw.setFooter('PDF conversion by xtopdf: https://google.com/search?q=xtopdf')

    with open(txt_filename) as txt_fil:
        for line in txt_fil:
            pw.writeLine(line.strip('\n'))
        pw.savePage()

def main():
    if len(sys.argv) != 2:
        usage(sys.argv)
        sys.exit(0)

    try:
        for filename in glob.glob(sys.argv[1]):
            print("Converting {} to {}".format(filename, filename + '.pdf'))
            text_to_pdf(filename)
    except Exception as e:
        print("Caught Exception: type: {}, message: {}".format(\
            e.__class__, str(e)))

if __name__ == '__main__':
    main()
