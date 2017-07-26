 Python 3.5.1 (v3.5.1:37a07cee5969, Dec  6 2015, 01:54:25) [MSC v.1900 64 bit (AMD64)] on win32
 Type "help", "copyright", "credits" or "license" for more information.
 >>> import fitz                                      # = PyMuPDF
 >>> doc = fitz.open("test.pdf")                      # open PDF
 >>> toc = doc.getToC()                               # get current table of contents
 >>> for t in toc: print(t)                           # show what we have so far
 ...
 [1, 'The PyMuPDF Documentation', 1]                  # = [hierarchy-level, title, page-number]
 [2, 'Introduction', 1]
 [3, 'Note on the Name fitz', 1]
 [3, 'License', 1]
 >>> toc[1][1] += " modified by setToC"               # modify anything
 >>> doc.setToC(toc)                                  # replace outline tree
 0
 >>> for t in doc.getToC(): print(t)                  # demonstrate it worked
 ...
 [1, 'The PyMuPDF Documentation', 1]
 [2, 'Introduction modified by setToC', 1]            # <<< this has changed!
 [3, 'Note on the Name fitz', 1]
 [3, 'License', 1]
 >>>
 >>> # similar for metadata:
 >>> doc.setMetadata({"author":"Jorj. X. McKie", "creator": ...})
 0
 >>> 
 >>> # when done, incrementally save to the file works in sub-second time
 >>> doc.save(doc.name, incremental=True)
 0
 >>>
