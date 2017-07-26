# -*- coding: Latin-1 -*-

"""
Convert OpenOffice documents to XML and text

USAGE:
ooconvert [filename]
"""

import zipfile
import re
import sys

rx_stripxml = re.compile("<[^>]*?>", re.DOTALL|re.MULTILINE)

class ReadOO:

    def __init__(self, filename):
        zf = zipfile.ZipFile(filename, "r")
        self.data = zf.read("content.xml")
        zf.close()

    def getXML(self):
        return self.data

    def getData(self, collapse=1):
        return " ".join(rx_stripxml.sub(" ", self.data).split())

if __name__=="__main__":
    if len(sys.argv)>1:
        oo = ReadOO(sys.argv[1])
        print oo.getXML()
        print oo.getData()
    else:
        print __doc__.strip()
