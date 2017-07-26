#!/usr/bin/env python

"""pdfpagecount.py - print number of pages in a PDF file.

This needs PyObjC 1.0 or higher. A more extended version might be
available one day here: http://python.net/~gherman
"""

__author__ = "Dinu C. Gherman"

import sys
from Foundation import NSData
from AppKit import NSPDFImageRep


def pageCount(pdfPath):
    "Return the number of pages for some PDF file."

    data = NSData.dataWithContentsOfFile_(pdfPath)
    img = NSPDFImageRep.imageRepWithData_(data)
    return img.pageCount()


if __name__ == '__main__':
    if len(sys.argv) == 2:
        print pageCount(sys.argv[1])
