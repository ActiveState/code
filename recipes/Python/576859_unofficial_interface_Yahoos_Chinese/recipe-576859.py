"""
    An unofficial interface of Yahoo's Chinese segmentation.

    * Before use it, you MUST specify your APPID in the code. * 

    Yahoo's api documents: http://tw.developer.yahoo.com/cas/
    
    Copyright 2009 Shao-Chuan Wang <shaochuan.wang@gmail.com>

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
    THE SOFTWARE.

"""
__author__ = "Shao-Chuan Wang"
__email__ = "shaochuan.wang@gmail.com"
__version__ = "1.0"
__URL__ = "http://shao-chuan.appspot.com"


import re
import codecs
import urllib, urllib2
import xml.etree.ElementTree as ETree

APPID = ''
API_URL = {'ws':'http://asia.search.yahooapis.com/cas/v1/ws',
           'ke':'http://asia.search.yahooapis.com/cas/v1/ke'}

class SegmentationResultXMLRetriever(object):
    url = API_URL['ws']
    def __init__(self, utf8String):
        d = {'appid'  : APPID,
             'content': utf8String }
        data = urllib.urlencode(list(d.iteritems()))
        req = urllib2.Request(type(self).url)
        fd = urllib2.urlopen(req, data)
        buf = []
        while True:
            data = fd.read(1024)
            if not len(data):
                break
            buf.append(data)

        self._xmlString = ''.join(buf)
    
    def getSegmentationXML(self):
        return self._xmlString

class WordSegmentationResultParser(object):
    tag_pat = re.compile(r'^[{].*[}]')
    @classmethod
    def fromstring(cls, rawString):
        ''' The factory method. '''
        obj = cls()
        obj._root = ETree.fromstring(rawString)
        objName, results = obj.makeObjectTree(obj._root)
        obj.results = results
        return obj

    def makeObjectTree(self, root):
        children = []
        d = {}  
        for c in root.getchildren():
            kvPair = self.makeObjectTree(c)
            if kvPair:
                d.setdefault(kvPair[0], kvPair[1])
                children.append(kvPair[1])
        v = root.text
        if v and v.isdigit():
            v = int(v)
        d.update({'children' : children,
                  'value'    : v })
        resultClassName = type(self).tag_pat.sub('', root.tag)
        resultObj = type(resultClassName,
                         (object, ),
                         d )
        return resultClassName.lower(), resultObj

    def getSegmentationResults(self):
        ''' This method has higher dependency on return xml file format.
        '''
        return [ x.token.value for x in self.results.children if bool(x.token.value) and x.token.value.strip() ]


if __name__ == '__main__':
    import os
    os.chdir(r'C:\python25')
    f = codecs.open('test.txt', 'r', 'utf-8')
    ustr = f.read()[1:]
    utf8str = codecs.encode(ustr, 'utf-8')
    f.close()

    # Here is the sample usage !
    retriever = SegmentationResultXMLRetriever(utf8str)
    c = retriever.getSegmentationXML()
    parser = WordSegmentationResultParser.fromstring(c)
    li = parser.getSegmentationResults()    
    print li
