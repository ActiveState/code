import sys
import pyPdf

def getPDFContent(path):
    content = ""
    # Load PDF into pyPDF
    pdf = pyPdf.PdfFileReader(file(path, "rb"))
    # Iterate pages
    for i in range(0, pdf.getNumPages()):
        # Extract text from page and add to content
        content += pdf.getPage(i).extractText() + " \n"
    # Collapse whitespace
    content = u" ".join(content.replace(u"\xa0", u" ").strip().split())
    return content

f = open(sys.argv[1]+'.txt','w+')
f.write(getPDFContent(sys.argv[1]))
f.close()
#print getPDFContent(sys.argv[1]).encode("ascii", "xmlcharrefreplace")
