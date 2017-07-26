"""
PrettyTableToPDF.py
A demo program to show how to convert the output generated 
by the PrettyTable library, to PDF, using the xtopdf toolkit 
for PDF creation from other formats.
Author: Vasudev Ram - http://www.dancingbison.com
xtopdf is at: http://slides.com/vasudevram/xtopdf

Copyright 2015 Vasudev Ram
"""

from prettytable import PrettyTable
from PDFWriter import PDFWriter

pt = PrettyTable(["City name", "Area", "Population", "Annual Rainfall"])
pt.align["City name"] = "l" # Left align city names
pt.padding_width = 1 # One space between column edges and contents (default)
pt.add_row(["Adelaide",1295, 1158259, 600.5])
pt.add_row(["Brisbane",5905, 1857594, 1146.4])
pt.add_row(["Darwin", 112, 120900, 1714.7])
pt.add_row(["Hobart", 1357, 205556, 619.5])
pt.add_row(["Sydney", 2058, 4336374, 1214.8])
pt.add_row(["Melbourne", 1566, 3806092, 646.9])
pt.add_row(["Perth", 5386, 1554769, 869.4])
lines = pt.get_string()

pw = PDFWriter('Australia-Rainfall.pdf')
pw.setFont('Courier', 12)
pw.setHeader('Demo of PrettyTable to PDF')
pw.setFooter('Demo of PrettyTable to PDF')
for line in lines.split('\n'):
    pw.writeLine(line)
pw.close()
