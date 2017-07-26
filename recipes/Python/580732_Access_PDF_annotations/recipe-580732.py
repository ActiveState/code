# loop through annotations of a page, change their author,
# make them 10% larger and save an image as PNG file
import fitz
doc    = fitz.open("some.pdf") # open the PDF
page   = doc[n]                # access page n (0-based)
annot  = page.firstAnnot       # get first annotation
matrix = fitz.Matrix(1.1, 1.1) # define matrix for scaling +10%
i      = 0                     # counter for file idents

# loop through the page's annotations
while annot:
    pix = annot.getPixmap(matrix = matrix)    # picture map for the annot
    pix.writePNG("annot-%s.png" % (str(i),))  # save it as PNG
    i += 1                                    # increase counter
    d = annot.info                            # get annot's info dictionary
    d["title"] = "Jorj X. McKie"              # set author (= popup title)
    annot.setInfo(d)                          # update info dict in annot 
    r = annot.rect * matrix                   # scale annot's rectangle
    annot.setRect(r)                          # store rect back in annot
    annot = annot.next                        # get next annot on page

# update PDF with the changes 
doc.saveIncr()
# alternatively, save to a new file:
doc.save("some-updates.pdf")
