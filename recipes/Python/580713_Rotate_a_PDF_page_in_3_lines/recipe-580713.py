import fitz                            # <- PyMuPDF v 1.9.3
doc = fitz.open("mypdf.pdf")           # open the PDF
page = doc[n]                          # read page n (zero-based)
page.setRotate(-90)                    # rotate page by 90 degrees counter-clockwise
doc.save(doc.name, incremental = True)  # update the file - a sub-second matter
doc.close()
