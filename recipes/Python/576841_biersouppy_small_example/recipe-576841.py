#!/usr/bin/env python
""" bier-soup.py: html tables -> text, a small example of BeautifulSoup
in: url or file like those in www.bier1.de
out:
    1   Adldorf     Graf Arco Pils      Graf ?
    ...
"""
# Schierlinger Pils: Think global, drink regional
# (a general html table <-> py table would be nice  and tough; see
# http://stackoverflow.com/questions/796490/python-method-to-extract-content-excluding-navigation-from-an-html-page


import re
from BeautifulSoup import BeautifulSoup
from collections import defaultdict

html = "http://www.bier1.de/L%E4nder%20gesamt/Bayern%20(Bavaria).htm"
# html = "Bier.html"
__date__ = "16jul 2009"
__author_email__ = "denis-bz-py@t-online.de"
Test = 1


#...............................................................................
def leaf( tag ):
    """ get text inside <tag><tag>... text """
    # <td>  <div><font size="2"><i><font color="#FFFFFF"> 
    #   + + + + +</font></i></font></div></td>
    # <td height="10"><font size="2"> Bierfeuerwerk <strong></strong> </font></td>

    for text in tag.findAll( text=True ):
        text = text.strip()
        if text:  return text
    return ""

def trow_cols( trow, td="td" ):
    """ soup.table.tr -> <td> leaf strings
    """
    if Test >= 2:
        print "test trow_cols:", trow.prettify()
    cols = []
    for col in trow( td ):
        text = leaf( col )
        text = re.sub( r"\s\s+", " ",  text.strip() )
        cols.append( text )
    return cols

def plus_num( s ):
    """ + + + + -  ->  5- """
    s = re.sub( r"\s+", "", s )
    if not s:
        return "- "
    if s[0] != "+":
        return s
    return "%d%s" % (len(s), "-" if s[-1] == "-"  else " ")

def biertext( row ):
    name, plus, stadt, kommentar = trow_cols( row )
    # [u'Kuchlbauer Helles Bier', u'+ + + + -', u'BY/Abensberg', u'Ein Schippe ...
    stadt = re.sub( "^BY/", "", stadt )
    note = plus_num( plus )
    return "%s  %s \t%s \t%s" % (note, stadt, name, kommentar)


#...............................................................................
if __name__ == "__main__":
    import codecs
    import sys
    import urllib2
    try:
        import bz.util as ut
        print ut.From()
        ut.ptime()
        jarg = ut.scan_eq_args( globals() )  # Test= ...
    except ImportError:
        ut = None
        jarg = 1
    if sys.argv[jarg:]:
        html = sys.argv[jarg]
    sys.stdout = codecs.getwriter("utf-8")(sys.__stdout__)

    if html.startswith( "http:" ):
        htmltext = urllib2.urlopen( html ) .read()
    else:
        htmltext = open( html ) .read()  # ut.openplus

    soup = BeautifulSoup( htmltext, convertEntities="html" )
    if ut:
        ut.ptime( "BeautifulSoup read %d bytes" % len(htmltext) )
            # 1m Bier.html ~ 20 sec mac g4 ppc

    table = soup.findAll( "table" )[1]  # skip table[0]
    rows = table( "tr" )
        # row 0 usually has <th> table headers, but not bier1.de
    th = trow_cols( rows[0], "th" ) or trow_cols( rows[0] )
    print "# table headers:", th
    for row in rows[1:]:
        print biertext( row )
    # | sort -k1rn

# end bier-soup.py
