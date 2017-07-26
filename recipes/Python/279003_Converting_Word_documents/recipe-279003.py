import fnmatch, os, pythoncom, sys, win32com.client

wordapp = win32com.client.gencache.EnsureDispatch("Word.Application")

try:
    for path, dirs, files in os.walk(sys.argv[1]):
        for doc in [os.path.abspath(os.path.join(path, filename)) for filename in files if fnmatch.fnmatch(filename, '*.doc')]:
            print "processing %s" % doc
            wordapp.Documents.Open(doc)
            docastxt = doc.rstrip('doc') + 'txt'
            wordapp.ActiveDocument.SaveAs(docastxt, FileFormat=win32com.client.constants.wdFormatTextLineBreaks)
            wordapp.ActiveWindow.Close()
finally:
    wordapp.Quit()
