## Print selected text pages to PDF with Python, selpg and xtopdf on Linux 
Originally published: 2014-10-29 17:38:09 
Last updated: 2014-10-29 17:38:10 
Author: Vasudev Ram 
 
This recipe shows how to use selpg, a Linux command-line utility written in C, together with xtopdf, a Python toolkit for PDF creation, to print only a selected range of pages from a text file, to a PDF file, for display or print purposes. The way to do this is to run the selpg utility at the Linux command line, with options specifying the start and end pages of the range, and pipe its output to the StdinToPDF.py program, which is a part of the xtopdf toolkit.\n