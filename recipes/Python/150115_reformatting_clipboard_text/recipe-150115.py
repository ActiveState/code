"""
  + This code reformats:

abc def
ghi kjl
ioe.

hoa aho
ulm dij.

  + into:

abc def ghi kjl ioe.

hoa aho ulm dij.
"""
import win32clipboard as w 
import win32con,re

def getText(): 
    w.OpenClipboard() 
    d=w.GetClipboardData(win32con.CF_TEXT) 
    w.CloseClipboard() 
    return d 
 
def setText(aType,aString): 
    w.OpenClipboard()
    w.EmptyClipboard()
    w.SetClipboardData(aType,aString) 
    w.CloseClipboard() 

def changeClipboardBy(aFunction):
    result=aFunction(getText().replace('\r\n','\n'))
    setText(win32con.CF_TEXT,result.replace('\n','\r\n'))

def paragraph(aString):
    aString=re.sub(r'(?m)^\s*$','',aString)
    aString=re.sub(r'(?<!\n)\n(?!\n|$)',' ',aString)
    return aString

if __name__=='__main__':
    changeClipboardBy(paragraph)
