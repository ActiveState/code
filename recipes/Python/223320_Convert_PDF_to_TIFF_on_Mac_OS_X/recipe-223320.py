#!/usr/bin/env python

"""pdf2tiff.py - convert PDF to TIFF on mac OS X.

This needs PyObjC 1.0 or higher. A more extended version will be soon
available on my Starship pages: http://python.net/~gherman/pdf2tiff.html
"""

__version__ = '0.5'
__author__ = 'Dinu C. Gherman'


from os.path import splitext
from objc import YES, NO
from Foundation import NSData
from AppKit import NSImage, NSPDFImageRep, NSApplication


NSApp = NSApplication.sharedApplication()

def pdf2tiff(pdfPath, pageNum=0, resolution=72.0):
    "Convert one page of a PDF to TIFF at a specific res. in DPI."

    tiffPath = "%s-%d.tiff" % (splitext(pdfPath)[0], pageNum)
    pdfData = NSData.dataWithContentsOfFile_(pdfPath)
    pdfRep = NSPDFImageRep.imageRepWithData_(pdfData)
    pageCount = pdfRep.pageCount()
    if pageNum > pageCount-1: return
    pdfRep.setCurrentPage_(pageNum)
    pdfImage = NSImage.alloc().init()
    pdfImage.addRepresentation_(pdfRep)
    originalSize = pdfImage.size()
    width, height = originalSize
    pdfImage.setScalesWhenResized_(YES)
    rf = resolution / 72.0
    pdfImage.setSize_((width*rf, height*rf))
    tiffData = pdfImage.TIFFRepresentation()
    tiffData.writeToFile_atomically_(tiffPath, YES)
