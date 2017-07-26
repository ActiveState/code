# a script that converts word file to txt files
# requires word application on Windows machine
# requirement:
#    1. Windows platform
#    2. python 2.7
#    3. pywin32, download from http://sourceforge.net/projects/pywin32/
#    4. word application installed on running machine
from win32com.client import constants, Dispatch
import pythoncom
import glob
import os
from zipfile import ZipFile

# convert the word file to a text file.
# @arg wordapp: The word IDispatch object
# @arg wordfile: The word file name
# @returns: The txt file name
def convert_to_text(wordapp, wordfile):
    name, ext = os.path.splitext(wordfile)
    if ext != '.doc' and ext != '.docx':
        return None
    txtfile = name + '.txt'
    print txtfile
    wordapp.Documents.Open(os.path.abspath(wordfile))
    wdFormatTextLineBreaks = 3
    wordapp.ActiveDocument.SaveAs(os.path.abspath(txtfile), 
	                              FileFormat=wdFormatTextLineBreaks)
    wordapp.ActiveDocument.Close()
    return txtfile

# a generator that iterates all doc files in the current work dir
def next_doc():
    for d in glob.glob('*.doc'):
        yield d
    for d in glob.glob('*.docx'):
        yield d

# convert all doc/docx files and zip all output txt files as the zipfilename
def convert_and_zip(zipfilename):
    word = Dispatch("Word.Application")
    with ZipFile(zipfilename, 'w') as fzip:
        for doc in next_doc():
            print 'converting ', doc, '...'
            txtfile = convert_to_text(word, doc)
            if txtfile:
                fzip.write(txtfile)
    word.Quit()
