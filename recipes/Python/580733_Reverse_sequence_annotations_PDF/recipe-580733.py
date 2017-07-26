import fitz
doc = fitz.open("some.pdf")      # open pdf
page = doc[n]                    # open the page (0-based number)
rtab = []                        # store all rectangles here
annot = page.firstAnnot          # read first annotation
while annot:
	rtab.append(annot.rect)  # store rectangle
	annot = annot.next       # read next annot

annot = page.firstAnnot          # cycle thru annots again
for rect in reversed(rtab):
	annot.setRect(rect)      # give it a new place
	annot = annot.next       
	
doc.save("some-reversed.pdf")    # save PDF with reversed annotations
