from __future__ import print_function

# BatchTextToPDF.py
# Convert a batch of text files to a single PDF.
# Each text file's content starts on a new page in the PDF file.
# Requires:
# - xtopdf: https://bitbucket.org/vasudevram/xtopdf
# - ReportLab: https://www.reportlab.com/ftp/reportlab-1.21.1.tar.gz
# Author: Vasudev Ram
# Copyright 2016 Vasudev Ram
# Product store: https://gumroad.com/vasudevram
# Web site: https://vasudevram.github.io
# Blog: http://jugad2.blogspot.com

import sys
import fileinput
from PDFWriter import PDFWriter

def usage(prog_name):
    sys.stderr.write("Usage: {} outfile.pdf infile1.txt ...".format(prog_name))

def main():

    if len(sys.argv) < 3:
        usage(sys.argv[0])
        sys.exit(0)

    try:
        pw = PDFWriter(sys.argv[1])
        pw.setFont('Courier', 12)
        pw.setFooter('xtopdf: https://google.com/search?q=xtopdf')

        for line in fileinput.input(sys.argv[2:]):
            if fileinput.filelineno() == 1:
                pw.setHeader(fileinput.filename())
                if fileinput.lineno() != 1:
                    pw.savePage()
            pw.writeLine(line.strip('\n'))

        pw.savePage()
        pw.close()
    except Exception as e:
        print("Caught Exception: type: {}, message: {}".format(\
            e.__class__, str(e)))

if __name__ == '__main__':
    main()
