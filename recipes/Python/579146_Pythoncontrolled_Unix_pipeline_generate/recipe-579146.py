# PopenToPDF.py
# Demo program to read text from a shell pipeline using 
# subprocess.Popen, and write the text to PDF using xtopdf.
# Author: Vasudev Ram
# Copyright (C) 2016 Vasudev Ram - http://jugad2.blogspot.com

import sys
import subprocess
from PDFWriter import PDFWriter

def error_exit(message):
    sys.stderr.write(message + '\n')
    sys.stderr.write("Terminating.\n")
    sys.exit(1)

def main():
    try:
        # Create and set up a PDFWriter instance.
        pw = PDFWriter("PopenTo.pdf")
        pw.setFont("Courier", 12)
        pw.setHeader("Use subprocess.Popen to read pipe and write to PDF.")
        pw.setFooter("Done using selpg, xtopdf, Python and ReportLab, on Linux.")

        # Set up a pipeline with nl and selpg such that we can read from its stdout.
        # nl numbers the lines of the input.
        # selpg extracts pages 3 to 5 from the input.
        pipe = subprocess.Popen("nl -ba 1000-lines.txt | selpg -s3 -e5", \
            shell=True, bufsize=-1, stdout=subprocess.PIPE, 
            stderr=sys.stderr).stdout

        # Read from the pipeline and write the data to PDF, using the PDFWriter instance.
        for idx, line in enumerate(pipe):
            pw.writeLine(str(idx).zfill(8) + ": " + line)
    except IOError as ioe:
        error_exit("Caught IOError: {}".format(str(ioe)))
    except Exception as e:
        error_exit("Caught Exception: {}".format(str(e)))
    finally:
        pw.close()

main()
