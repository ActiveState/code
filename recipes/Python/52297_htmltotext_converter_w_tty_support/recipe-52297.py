#!/usr/bin/env python
# htmltotext

import sys, os, htmllib, formatter

bold = os.popen('tput bold').read()
underline =  os.popen('tput smul').read()
reset = os.popen('tput sgr0').read()

class TtyFormatter(formatter.AbstractFormatter):
    def __init__(self, writer):
	formatter.AbstractFormatter.__init__(self, writer)
	self.fontStack = []
	self.fontState = (0,0)
    def push_font(self, font):
	size, italic, bold, tt = font
	self.fontStack.append((italic, bold))
	self.updateFontState()
    def pop_font(self, *args):
	try: self.fontStack.pop()
	except: pass
	self.updateFontState()
    def updateFontState(self):
	try: newState = self.fontStack[-1]
	except: newState = (0,0)
	if self.fontState != newState:
	    print reset,
	    if newState[0]: print underline,
	    if newState[1]: print bold,
	    self.fontState = newState

myWriter = formatter.DumbWriter()
if sys.stdout.isatty():
    myFormatter = TtyFormatter(myWriter)
else:
    myFormatter = formatter.AbstractFormatter(myWriter)
myParser = htmllib.HTMLParser(myFormatter)
myParser.feed(sys.stdin.read())
myParser.close()
