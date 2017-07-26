#! /usr/bin python
# -*- coding: utf-8 -*-
"""
@created: 2016-04-23 13:40:00
@updated: 1016-08-25 20:00:00
@author: Jorj X. McKie

Find all fonts used in a PDF.
"""
from __future__ import print_function
import fitz                       # PyMuPDF

doc = fitz.open("file.pdf")

for i in len(doc):
    fontlist = doc.getPageFontList(i)
    if fontlist:
        print("fonts used on page", i)
    for font in fontlist:
        print("xref=%s, gen=%s, type=%s, basefont=%s, name=%s" % (font[0], font[1], font[2], font[3], font[4]))
