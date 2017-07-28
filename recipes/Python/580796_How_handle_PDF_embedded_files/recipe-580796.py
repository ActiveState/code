import fitz                      # = PyMuPDF
doc = fitz.open("test.pdf")      # open the PDF
count = doc.embeddedFileCount
print("number of embedded file:", count)     # shows number of embedded files

# get decompressed content of data stored by name "my data"
# also possible to use integer between 0 and "count - 1"

buff = doc.embeddedFileGet("my data")
fout = open("test.file", "wb")   # open output file
fout.write(buff)
fout.close()
