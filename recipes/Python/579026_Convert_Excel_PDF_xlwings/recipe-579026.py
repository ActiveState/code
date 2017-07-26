"""
xlwingsToPDF.py
A demo program to show how to convert the text extracted from Excel 
content, using xlwings, to PDF. It uses the xlwings library, to create 
and read the Excel input, and the xtopdf library to write the PDF output.
Author: Vasudev Ram - http://www.dancingbison.com
Copyright 2015 Vasudev Ram
"""

import sys
from xlwings import Workbook, Sheet, Range, Chart
from PDFWriter import PDFWriter

# Create a connection with a new workbook.
wb = Workbook()

# Create the Excel data.
# Column 1.
Range('A1').value = 'Foo 1'
Range('A2').value = 'Foo 2'
Range('A3').value = 'Foo 3'
# Column 2.
Range('B1').value = 'Bar 1'
Range('B2').value = 'Bar 2'
Range('B3').value = 'Bar 3'

pw = PDFWriter("xlwingsTo.pdf")
pw.setFont("Courier", 10)
pw.setHeader("Testing Excel conversion to PDF with xlwings and xtopdf")
pw.setFooter("xlwings: http://xlwings.org --- xtopdf: http://slid.es/vasudevram/xtopdf")

for row in Range('A1..B3').value:
    s = ''
    for col in row:
        s += col + ' | '
    pw.writeLine(s)

pw.close()
