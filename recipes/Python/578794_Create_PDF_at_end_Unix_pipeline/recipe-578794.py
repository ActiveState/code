# StdinToPDF.py

# Read the contents of stdin (standard input) and write it to a PDF file 
# whose name is specified as a command line argument.
# Author: Vasudev Ram - http://www.dancingbison.com
# This program is part of the xtopdf toolkit:
#     https://bitbucket.org/vasudevram/xtopdf

import sys
from PDFWriter import PDFWriter

try:
    with PDFWriter(sys.argv[1]) as pw:
        pw.setFont("Courier", 12)
        for lin in sys.stdin:
            pw.writeLine(lin)
except Exception, e:
    print "ERROR: Caught exception: " + repr(e)
    sys.exit(1)
