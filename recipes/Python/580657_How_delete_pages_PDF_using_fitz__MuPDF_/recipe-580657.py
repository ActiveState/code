import fitz                             # this is PyMuPDF 1.9.0
doc = fitz.open("some.pdf")

# An easy start: create new PDFs of the first and last 10 pages ...
l = list(range(10))                     # first 10 pages
doc.select(l)                           # delete all others
doc.save("some-first-10.pdf", garbage=3)# save and clean new PDF
doc.close()
doc = fitz.open("some.pdf")             # recycle PDF
l = list(range(doc.pageCount-10, doc.pageCount))    # last 10 pages
doc.select(l)                           # delete all others
doc.save("some-last-10.pdf", garbage=3) # save and clean new PDF
doc.close()

# page numbers may occur multiple times and in any order ...
doc = fitz.open("some.pdf")             # recycle PDF
doc.select([1,1,1,3,3,3,5,5,5,0,0,0])   # create crazily tripled pages
doc.save("some-crazy-triples.pdf", garbage=3)   # save that & clean new PDF
doc.close()

# new PDF containing the original 2 times
doc = fitz.open("some.pdf")             # recycle PDF
l = list(range(doc.pageCount))          # list of all pages
l += l                                  # two times that [0,...,n,0,...,n]
doc.select(l)                           # PDF will now contain itself twice ...
doc.save("some-times-2.pdf")            # will hardly be bigger than original!
doc.close()

# delete pages without text (or whatever ...)
doc = fitz.open("some.pdf")             # recycle PDF
l = list(range(doc.pageCount))          # list of all pages
for i in l:
    if not doc.getPageText(i)           # if no text on page number i ...
        l.remove(i)                     # delete that page from list
doc.select(l)                           # select remaining pages from the PDF
doc.save("some-non-empty.pdf", garbage=3)         # save PDF, every page has some text now ...
doc.close()
