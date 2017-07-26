#!/usr/bin/env python
"""
    Modul:          xmlgettext.py
    Description:    Erzeugt aus dem Textinhalt einer XML-Datei ein *.pot
                    nicht zu extrahierende Texte koennen mit einem <!--!-->
                    Kommentar markiert werden.
    Version:        V1.0b
    Copyright:      2003 by Fritz Cizmarov fritz@sol.at
    License:        GPL
"""

from xml.parsers import expat
from htmlentitydefs import entitydefs

class XMLTextParser:
    def __init__(self, file):
        self.strings = []
        self.current = []
        self.no_translate = []
        
        self.parser = expat.ParserCreate()
        self.parser.StartElementHandler = self.Start_Elem_Handler
        self.parser.EndElementHandler = self.End_Elem_Handler
        self.parser.CharacterDataHandler = self.Char_Data_Handler
        self.parser.DefaultHandler = self.Default_Handler
        self.parser.CommentHandler = self.Comment_Handler

        fopen = 0
        if type(file) is str:
            file = open(file)
            fopen = 1
        self.parser.ParseFile(file)
        if fopen:
            file.close()

    def Start_Elem_Handler(self, name, attrs):
        if name != "br": # bei <br/> gibts nix zu tun
            nt = attrs.get("no_translate", "no") in ["yes", "true"]
            self.no_translate.append(nt)
            self.current.append("")
        
    def End_Elem_Handler(self, name):
        if name == "br": # bei <br/> ein nl anhaengen
            self.current[-1] += "\n"
        else:
            res = self.current.pop().strip()
            if res != "":
                self.strings.append(res)
            self.no_translate.pop()
    
    def Char_Data_Handler(self, data):
        if not self.no_translate[-1]:
            self.current[-1] += data.strip("\t").replace("\n", " ")

    def Default_Handler(self, data):
        if data[0] == "&" and data[-1] == ";":
            self.current[-1] += unicode(entitydefs[data[1:-1]], 'iso-8859-15')
        
    def Comment_Handler(self, data):
        if data == "!":
            self.no_translate[-1] = 1
    
import sys, time, locale

if len(sys.argv) == 1 or sys.argv[0] in ["-h","--help"]:
    print "Usage: xmlgettext.py infile [outfile]"
    sys.exit()
elif len(sys.argv) == 3:
    out = open(sys.argv[2],"w")
else:
    out = sys.stdout
    
p = XMLTextParser(sys.argv[1])

datetime = time.strftime(locale.nl_langinfo(locale.D_T_FMT))
codeset = locale.getdefaultlocale()

out.write("# SOME DESCRIPTIVE TITLE.\n")
out.write("# Copyright (C) YEAR ORGANIZATION\n")
out.write("# FIRST AUTHOR <EMAIL@ADDRESS>, YEAR.\n")
out.write("#\n")
out.write('msgid ""\n')
out.write('msgstr""\n')
out.write('"Project-Id-Version: PACKAGE VERSION\\n"\n')
out.write('"POT-Creation-Date: '+datetime+'\\n"\n')
out.write('"PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\\n"\n')
out.write('"Last-Translator: FULL NAME <EMAIL@ADDRESS>\\n"\n')
out.write('"Language-Team: LANGUAGE <LL@li.org>\\n"\n')
out.write('"MIME-Version: 1.0\\n"\n')
out.write('"Content-Type: text/plain; charset='+codeset[1]+'\\n"\n')
out.write('"Content-Transfer-Encoding: 8bit\\n"\n')
out.write('"Generated-By: xmlgettext.py 1.4\\n"\n')


for string in p.strings:
    quote = '"' in string and "'" or '"'
    out.write('msgid '+quote+string.replace('\n', '\\n')+quote+'\n')
    out.write('msgstr '+quote*2+'\n'*2)

if out != sys.stdout:
    out.close()
