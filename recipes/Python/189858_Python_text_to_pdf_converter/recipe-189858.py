"""
 pyText2Pdf - Python script to convert plain text files into Adobe
 Acrobat PDF files.

 Version 1.2

 Author: Anand B Pillai <abpillai at lycos dot com>
 Keywords: python, tools, converter, pdf, text2pdf, adobe, acrobat,
           processing.

 Copyright (C) 2003-2004 Free Software Foundation, Inc.

 This file is free software; you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation; either version 2, or (at your option)
 any later version.

 This file is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.
    
 You should have received a copy of the GNU General Public License
 along with GNU Emacs; see the file COPYING.  If not, write to
 the Free Software Foundation, Inc., 59 Temple Place - Suite 330,
 Boston, MA 02111-1307, USA.
    
 Commentary:

 Modification History:

 Mon Feb 17 12:20:13 2003 Changed option parsing algorithm to use
                          getopt. Use __main__ calling convention.
                          Bug in FF character fixed.
 Thu Apr 10 11:26:58 2003 Modified to use python style strings
                          and function objects.
 July 1 2003              Fixed help string errors. Added the
                          Creator property.
 Feb 25 2004              Rewrote argument parser to remove
                          duplicate code.Use string.join() instead
                          of concatenation. Modified sys.exit()
                          calls to print messages.
    Code:
"""

# http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/189858

import sys, os
import string
import time
import getopt

LF_EXTRA=0
LINE_END='\015'
# form feed character (^L)
FF=chr(12)

ENCODING_STR = """\
/Encoding <<
/Differences [ 0 /.notdef /.notdef /.notdef /.notdef
/.notdef /.notdef /.notdef /.notdef /.notdef /.notdef
/.notdef /.notdef /.notdef /.notdef /.notdef /.notdef
/.notdef /.notdef /.notdef /.notdef /.notdef /.notdef
/.notdef /.notdef /.notdef /.notdef /.notdef /.notdef
/.notdef /.notdef /.notdef /.notdef /space /exclam
/quotedbl /numbersign /dollar /percent /ampersand
/quoteright /parenleft /parenright /asterisk /plus /comma
/hyphen /period /slash /zero /one /two /three /four /five
/six /seven /eight /nine /colon /semicolon /less /equal
/greater /question /at /A /B /C /D /E /F /G /H /I /J /K /L
/M /N /O /P /Q /R /S /T /U /V /W /X /Y /Z /bracketleft
/backslash /bracketright /asciicircum /underscore
/quoteleft /a /b /c /d /e /f /g /h /i /j /k /l /m /n /o /p
/q /r /s /t /u /v /w /x /y /z /braceleft /bar /braceright
/asciitilde /.notdef /.notdef /.notdef /.notdef /.notdef
/.notdef /.notdef /.notdef /.notdef /.notdef /.notdef
/.notdef /.notdef /.notdef /.notdef /.notdef /.notdef
/dotlessi /grave /acute /circumflex /tilde /macron /breve
/dotaccent /dieresis /.notdef /ring /cedilla /.notdef
/hungarumlaut /ogonek /caron /space /exclamdown /cent
/sterling /currency /yen /brokenbar /section /dieresis
/copyright /ordfeminine /guillemotleft /logicalnot /hyphen
/registered /macron /degree /plusminus /twosuperior
/threesuperior /acute /mu /paragraph /periodcentered
/cedilla /onesuperior /ordmasculine /guillemotright
/onequarter /onehalf /threequarters /questiondown /Agrave
/Aacute /Acircumflex /Atilde /Adieresis /Aring /AE
/Ccedilla /Egrave /Eacute /Ecircumflex /Edieresis /Igrave
/Iacute /Icircumflex /Idieresis /Eth /Ntilde /Ograve
/Oacute /Ocircumflex /Otilde /Odieresis /multiply /Oslash
/Ugrave /Uacute /Ucircumflex /Udieresis /Yacute /Thorn
/germandbls /agrave /aacute /acircumflex /atilde /adieresis
/aring /ae /ccedilla /egrave /eacute /ecircumflex
/edieresis /igrave /iacute /icircumflex /idieresis /eth
/ntilde /ograve /oacute /ocircumflex /otilde /odieresis
/divide /oslash /ugrave /uacute /ucircumflex /udieresis
/yacute /thorn /ydieresis ]
>>
"""


PROG_HELP = """\

%(progname)s  [options] [filename]

%(progname)s  makes a 7-bit clean PDF file from any input file.

It reads from a named file, and writes the PDF file to a file specified by 
the user, otherwise to a file with '.pdf' appended to the input file.

Author: Anand B Pillai.

Copyright (C) 2003-2004 Free Software Foundation, http://www.fsf.org

There are various options as follows:

  -h\t\tshow this message\n
  -o/-O\t\tdirect output to this file
  -f<font>\tuse PostScript <font> (must be in standard 14, default: Courier)
  -I\t\tuse ISOLatin1Encoding
  -s<size>\tuse font at given pointsize (default 10) points\n
  -v<dist>\tuse given line spacing (default 12) points
  -l<lines>\tlines per page (default 60, determined automatically\n\t\tif unspecified)
  -c<chars>\tmaximum characters per line (default 80)
  -t<spaces>\tspaces per tab character (default 4)
  -F\t\tignore formfeed characters (^L)
    \t\t(i.e, accept formfeed characters as pagebreaks)\n
  -A4\t\tuse A4 paper (default Letter)
  -A3\t\tuse A3 paper (default Letter)
  -x<width>\tindependent paper width in points
  -y<height>\tindependent paper height in points
  -2\t\tformat in 2 columns
  -L\t\tlandscape mode

Note that where one variable is implied by two options, the second option
takes precedence for that variable. (e.g. -A4 -y500)

In landscape mode, page width and height are simply swapped over before
formatting, no matter how or when they were defined.
"""


class pyText2Pdf:

    def __init__(self):
        # version number
        self._version="1.1.1"
        # iso encoding flag
        self._IsoEnc=0
        # formfeeds flag
        self._doFFs=0
        self._progname="PyText2Pdf"
        self._appname = "".join((self._progname, " Version ", str(self._version)))
        # default font
        self._font="/Courier"
        # default font size
        self._ptSize=10
        # default vert space
        self._vertSpace=12
        self._lines=0
        # number of characters in a row
        self._cols=80
        self._columns=1
        # page ht
        self._pageHt=792
        # page wd
        self._pageWd=612
        # input file 
        self._ifile=""
        # output file 
        self._ofile=""
        # default tab width
        self._tab=4
        # input file descriptor
        self._ifs=None
        # output file descriptor
        self._ofs=None
        # landscape flag
        self._landscape=0

        # marker objects
        self._curobj = 5
        self._pageObs = [0]
        self._locations = [0,0,0,0,0,0]
        self._pageNo=0

        # file position marker
        self._fpos=0

    def argsCallBack(self, argslist, listoftuples=False):
        """ Callback function called by argument parser.
        Helps to remove duplicate code """

        x = 0
        while x<len(argslist):
            item = argslist[x]

            if listoftuples:
                o, a = item
            else:
                o = item

            if o == '-h':
                self.ShowHelp()
            elif o == '-I':
                self._IsoEnc=1
            elif o == '-F':
                self._doFFs=1
            elif o == '-2':
                self._columns=2
            elif o == '-L':
                self._landscape=1
                    
            if o in ('-f', '-s', '-l', '-x', 'y', '-c', '-v', '-o', '-O'):
                
                if not listoftuples:
                    x += 1
                    try:
                        a = argslist[x]
                    except:
                        msg = "Argument error for option " + o
                        sys.exit(msg)

                if a == "" or a[0] == "-":
                    msg = "Error: argument error for option " + o
                    sys.exit(msg)
                elif o == '-f':
                    self._font='/' + a
                elif o == '-A':
                    if a == '3':
                        self._pageWd=842
                        self._pageHt=1190
                    elif a =='4':
                        self._pageWd=595
                        self._pageHt=842
                    else:
                        psz=o[1]+a
                        print self._progname, ': ignoring unknown paper size ', psz
                elif o == '-s':
                    self._ptSize=int(a)
                    if self._ptSize<1:
                        self._ptSize=1
                elif o == '-v':
                    self._vertSpace=int(a)
                    if self._vertSpace<1:
                        self._vertSpace=1       
                elif o == '-l':
                    self._lines=int(a)
                    if self._lines<1:
                        self._lines=1
                elif o == '-c':
                    self._cols=int(a)
                    if self._cols<4:
                        self._cols=4
                elif o == '-t':
                    self._tab=int(a)
                    if self._tab<1:
                        self._tab=1
                elif o == '-x':
                    self._pageWd=int(a)
                    if self._pageWd<72:
                        self._pageWd=72
                elif o == '-y':
                    self._pageHt=int(a)
                    if self._pageHt<72:
                        self._pageHt=72
                elif o in ('-o', '-O'):
                    self._ofile=a
                else:
                    print self._progname, ': ignoring invalid switch: ', o

            x += 1

        
    def parseArgs(self):

        if len(sys.argv) == 1:
            self.ShowHelp()

        arguments=sys.argv[1:]
        
        optlist, args = getopt.getopt(arguments, 'hIF2Lf:A:s:v:l:c:t:x:y:o:')
        
        # input file is the first element in arg list
        # or last element in options list (in case of an error!)
        if len(args):
            self._ifile=args[0]
        else:
            l=len(optlist)
            tup=optlist[l-1]

        # parse options list
        if len(optlist):
            self.argsCallBack( optlist, listoftuples=True )
        else:
            self.argsCallBack( args )

        if self._landscape:
            print 'Landscape option on...'
        if self._columns==2:
            print 'Printing in two columns...'
        if self._doFFs:
            print 'Ignoring form feed character...'
        if self._IsoEnc:
            print 'Using ISO Latin Encoding...'
        print 'Using font', self._font[1:], ' size =', self._ptSize
            

    def writestr(self, str):
        """ Write string to output file descriptor.
        All output operations go through this function.
        We keep the current file position also here"""

        # update current file position
        self._fpos += len(str)
        for x in range(0, len(str)):
            if str[x] == '\n':
                self._fpos += LF_EXTRA
        try:
            self._ofs.write(str)
        except IOError, e:
            print e
            return -1

        return 0
            
    def Convert(self):
        """ Perform the actual conversion """
    
        if self._landscape:
            # swap page width & height
            tmp = self._pageHt
            self._pageHt = self._pageWd
            self._pageWd = tmp

        if self._lines==0:
            self._lines = (self._pageHt - 72)/self._vertSpace
        if self._lines < 1:
            self._lines=1
        
        try:
            self._ifs=open(self._ifile)
        except IOError, (strerror, errno):
            print 'Error: Could not open file to read --->', self._ifile
            sys.exit(3)

        if self._ofile=="":
            self._ofile=self._ifile + '.pdf'

        try:
            self._ofs = open(self._ofile, 'wb')
        except IOError, (strerror, errno):
            print 'Error: Could not open file to write --->', self._ofile
            sys.exit(3)

        print 'Input file =>', self._ifile
        print 'Writing pdf file', self._ofile, '...'
        self.WriteHeader(self._ifile)
        self.WritePages()
        self.WriteRest()

        print 'Wrote file', self._ofile
        self._ifs.close()
        self._ofs.close()
        return 0

    def WriteHeader(self, title):
        """Write the PDF header"""

        ws = self.writestr

        t=time.localtime()
        timestr=str(time.strftime("D:%Y%m%d%H%M%S", t))
        ws("%PDF-1.4\n")
        self._locations[1] = self._fpos
        ws("1 0 obj\n")
        ws("<<\n")

        buf = "".join(("/Creator (", self._appname, " By Anand B Pillai )\n"))
        ws(buf)
        buf = "".join(("/CreationDate (", timestr, ")\n"))
        ws(buf)
        buf = "".join(("/Producer (", self._appname, "(\\251 Free Software Foundation, 2004))\n"))
        ws(buf)
        
        if title:
            buf = "".join(("/Title (", title, ")\n"))
            ws(buf)

        ws(">>\n")
        ws("endobj\n")
    
        self._locations[2] = self._fpos

        ws("2 0 obj\n")
        ws("<<\n")
        ws("/Type /Catalog\n")
        ws("/Pages 3 0 R\n")
        ws(">>\n")
        ws("endobj\n")
        
        self._locations[4] = self._fpos
        ws("4 0 obj\n")
        ws("<<\n")
        buf = "".join(("/BaseFont ", str(self._font), " /Encoding /WinAnsiEncoding /Name /F1 /Subtype /Type1 /Type /Font >>\n"))
        ws(buf)
    
        if self._IsoEnc:
            ws(ENCODING_STR)
            
        ws(">>\n")
        ws("endobj\n")
        
        self._locations[5] = self._fpos
        
        ws("5 0 obj\n")
        ws("<<\n")
        ws("  /Font << /F1 4 0 R >>\n")
        ws("  /ProcSet [ /PDF /Text ]\n")
        ws(">>\n")
        ws("endobj\n")
    
    def StartPage(self):
        """ Start a page of data """

        ws = self.writestr
        
        self._pageNo += 1
        self._curobj += 1

        self._locations.append(self._fpos)
        self._locations[self._curobj]=self._fpos
    
        self._pageObs.append(self._curobj)
        self._pageObs[self._pageNo] = self._curobj
        
        buf = "".join((str(self._curobj), " 0 obj\n"))

        ws(buf)
        ws("<<\n")
        ws("/Type /Page\n")
        ws("/Parent 3 0 R\n")
        ws("/Resources 5 0 R\n")

        self._curobj += 1
        buf = "".join(("/Contents ", str(self._curobj), " 0 R\n"))
        ws(buf)
        ws(">>\n")
        ws("endobj\n")
        
        self._locations.append(self._fpos)
        self._locations[self._curobj] = self._fpos

        buf = "".join((str(self._curobj), " 0 obj\n"))
        ws(buf)
        ws("<<\n")
        
        buf = "".join(("/Length ", str(self._curobj + 1), " 0 R\n"))
        ws(buf)
        ws(">>\n")
        ws("stream\n")
        strmPos = self._fpos
    
        ws("BT\n");
        buf = "".join(("/F1 ", str(self._ptSize), " Tf\n"))
        ws(buf)
        buf = "".join(("1 0 0 1 50 ", str(self._pageHt - 40), " Tm\n"))
        ws(buf)
        buf = "".join((str(self._vertSpace), " TL\n"))
        ws(buf)
    
        return strmPos

    def EndPage(self, streamStart):
        """End a page of data """
        
        ws = self.writestr

        ws("ET\n")
        streamEnd = self._fpos
        ws("endstream\n")
        ws("endobj\n")
    
        self._curobj += 1
        self._locations.append(self._fpos)
        self._locations[self._curobj] = self._fpos
    
        buf = "".join((str(self._curobj), " 0 obj\n"))
        ws(buf)
        buf = "".join((str(streamEnd - streamStart), '\n'))
        ws(buf)
        ws('endobj\n')
    
    def WritePages(self):
        """Write pages as PDF"""
        
        ws = self.writestr

        beginstream=0
        lineNo, charNo=0,0
        ch, column=0,0
        padding,i=0,0
        atEOF=0
        
        while not atEOF:
            beginstream = self.StartPage()
            column=1
            
            while column <= self._columns:
                column += 1
                atFF=0
                atBOP=0
                lineNo=0
            
                while lineNo < self._lines and not atFF and not atEOF:
                    
                    lineNo += 1
                    ws("(")
                    charNo=0
                    
                    while charNo < self._cols:
                        charNo += 1
                        ch = self._ifs.read(1)
                        cond = ((ch != '\n') and not(ch==FF and self._doFFs) and (ch != ''))
                        if not cond:
                            break

                        if ord(ch) >= 32 and ord(ch) <= 127:
                            if ch == '(' or ch == ')' or ch == '\\':
                                ws("\\")
                            ws(ch)
                        else:
                            if ord(ch) == 9:
                                padding =self._tab - ((charNo - 1) % self._tab)
                                for i in range(padding):
                                    ws(" ")
                                charNo += (padding -1)
                            else:
                                if ch != FF:
                                    # write \xxx form for dodgy character
                                    buf = "".join(('\\', ch))
                                    ws(buf)
                                else:
                                    # dont print anything for a FF
                                    charNo -= 1

                    ws(")'\n")
                    if ch == FF:
                        atFF=1
                    if lineNo == self._lines:
                        atBOP=1
                        
                    if atBOP:
                        pos=0
                        ch = self._ifs.read(1)
                        pos= self._ifs.tell()
                        if ch == FF:
                            ch = self._ifs.read(1)
                            pos=self._ifs.tell()
                        # python's EOF signature
                        if ch == '':
                            atEOF=1
                        else:
                            # push position back by one char
                            self._ifs.seek(pos-1)

                    elif atFF:
                        ch = self._ifs.read(1)
                        pos=self._ifs.tell()
                        if ch == '':
                            atEOF=1
                        else:
                            self._ifs.seek(pos-1)

                if column < self._columns:
                    buf = "".join(("1 0 0 1 ",
                                   str((self._pageWd/2 + 25)),
                                   " ",
                                   str(self._pageHt - 40),
                                   " Tm\n"))
                    ws(buf)

            self.EndPage(beginstream)

    def WriteRest(self):
        """Finish the file"""

        ws = self.writestr
        self._locations[3] = self._fpos
    
        ws("3 0 obj\n")
        ws("<<\n")
        ws("/Type /Pages\n")
        buf = "".join(("/Count ", str(self._pageNo), "\n"))
        ws(buf)
        buf = "".join(("/MediaBox [ 0 0 ", str(self._pageWd), " ", str(self._pageHt), " ]\n"))
        ws(buf)
        ws("/Kids [ ")
    
        for i in range(1, self._pageNo+1):
            buf = "".join((str(self._pageObs[i]), " 0 R "))
            ws(buf)

        ws("]\n")
        ws(">>\n")
        ws("endobj\n")
        
        xref = self._fpos
        ws("xref\n")
        buf = "".join(("0 ", str((self._curobj) + 1), "\n"))
        ws(buf)
        buf = "".join(("0000000000 65535 f ", str(LINE_END)))
        ws(buf)

        for i in range(1, self._curobj + 1):
            val = self._locations[i]
            buf = "".join((string.zfill(str(val), 10), " 00000 n ", str(LINE_END)))
            ws(buf)

        ws("trailer\n")
        ws("<<\n")
        buf = "".join(("/Size ", str(self._curobj + 1), "\n"))
        ws(buf)
        ws("/Root 2 0 R\n")
        ws("/Info 1 0 R\n")
        ws(">>\n")
        
        ws("startxref\n")
        buf = "".join((str(xref), "\n"))
        ws(buf)
        ws("%%EOF\n")
        
    def ShowHelp(self):
        """Show help on this program"""
        
        sys.exit( PROG_HELP % {'progname': self._progname} )

def main():
    
    pdfclass=pyText2Pdf()
    pdfclass.parseArgs()
    pdfclass.Convert()

if __name__ == "__main__":
    main()
