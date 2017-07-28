import fitz                           # import PyMuPDF
doc = fitz.open("some.pdf")           # or new: fitz.open(), followed by insertPage()
page = doc[n]                         # choose some page
rect = fitz.Rect(50, 100, 300, 400)   # rectangle (left, top, right, bottom) in pixels

text = """This text will only appear in the rectangle. Depending on width, new lines are generated as required.\n<- This forced line break will also appear.\tNow a very long word: abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ.\nIt will be broken into pieces."""

rc = page.insertTextbox(rect, text, fontsize = 12, # choose fontsize (float)
                   fontname = "Times-Roman",       # a PDF standard font
                   fontfile = None,                # could be a file on your system
                   align = 0)                      # 0 = left, 1 = center, 2 = right

print("unused rectangle height: %g" % rc)          # just demo (should display "44.2")

doc.saveIncr()   # update file. Save to new instead by doc.save("new.pdf",...)
