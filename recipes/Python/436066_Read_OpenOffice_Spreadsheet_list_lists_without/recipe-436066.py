#! /usr/bin/env python
#
# -*- coding: latin1 -*-
"""
Read OpenOffice spreadsheets.

Read OpenOffice spreadsheets. Can be used as a module: it provides the
class OOspreadData which is simply a list of lists initialized with the
contents of the spreadsheet stored in a (typically .sxc) file (passed as an
argument).

Used as an executable, converts files.sxc to csv

USAGE:
readsxc file.sxc
"""

import sys

class ReadSXCError(Exception):
    pass

import xml.parsers.expat
import zipfile

tabla=[]
row=[]
cell=u''
rept=u'table:number-columns-repeated'
last_repeat_col=0
incol=False
compact=False
str_strip=False

def copyandtrim(l, trim):
    a = l[:]
    if trim:
        x=range(len(a))
        x.reverse()
        for i in x:
            if a[i]=="":
                del a[i]
            else:
                break
    return a

# 3 handler functions
def start_element(name, attrs):
    global tabla, row, cell, rept, last_repeat_col, incol, compact
    if name!="table:table-cell":
        return
    if incol:
        raise ReadSXCError("double cell start")
    incol=True
    cell=u""
    if attrs.has_key(rept):
        last_repeat_col = int(attrs[rept])
    else:
        last_repeat_col = 0

def end_element(name):
    global tabla, row, cell, rept, last_repeat_col, incol, compact, str_strip
    if name=="table:table-cell":
        if not incol:
            raise ReadSXCError("double cell end")
        incol=False
        # add the contents to the row
        if str_strip:
            row.append(cell.strip())
        else:
            row.append(cell)
        # print "append to row %d, col %d : %s" % (len(tabla),len(row),cell)
        # manage the repeater
        if last_repeat_col > 1:
            row.extend([cell]*(last_repeat_col-1))
    elif name=="table:table-row":
        l = copyandtrim(row,compact)
        if l == []:
            row = []
            return
        tabla.append(l)
        row = []

def char_data(data):
    global tabla, row, cell, rept, last_repeat_col, incol
    if incol:
        cell += data


def read_and_parse(inFileName):
    p = xml.parsers.expat.ParserCreate("UTF-8")
    p.StartElementHandler = start_element
    p.EndElementHandler = end_element
    p.CharacterDataHandler = char_data
    zf = zipfile.ZipFile(inFileName, "r")
    all = zf.read("content.xml")
    # Start the parse.
    p.returns_unicode=1
    p.Parse(all)
    zf.close()


class OOSpreadData(list):
    """OOspreadData: a=OOspreadData("file",trim=True,strip=False)

the class OOspreadData which is simply a list of lists initialized with the
contents of the spreadsheet stored in a (typically .sxc) file (passed as an
argument). Note: there is no validity analysis on the data.
Garbage in, garbage out, or unexepected execptions.

If trim is true, multiple void cell at the end of a row and void rows are
trimmed out; otherwise, all the cells are reported.

If strip is true, every cell content is stripped of blanks.
    """

    def __init__(self, fname,trim=True,strip=False):
        global tabla, row, cell, rept, last_repeat_col, incol, compact, str_strip
        tabla=[]
        row=[]
        incol=False
        cell=u''
        last_repeat_col=0
        compact=trim
        str_strip=strip
        # ok, do the hard work
        read_and_parse(fname)
        list.__init__(self, tabla)

if __name__=="__main__":

    if len(sys.argv)==2:
        oosxc = readsxc.OOSpreadData(sys.argv[1])
    else:
        print >> sys.stderr, "Usage: %s <OO_calc_file>" % sys.argv[0]
        sys.exit(1)

        for l in oosxc:
            a = ['"%s"' % i for i in l]
            print ",".join(a)

    sys.exit(0)
