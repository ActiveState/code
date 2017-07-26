import fitz                          # <-- PyMuPDF
doc = fitz.open("some.pdf")          # open the PDF
rect = fitz.Rect(0, 0, 100, 100)     # where to put image: use upper left corner

for page in doc:
    page.insertImage(rect, filename = "some.image")

doc.saveIncr()                       # do an incremental save
