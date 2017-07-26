from reportlab.pdfgen import canvas
from reportlab.lib.units import mm

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        """add page info to each page (page x of y)"""
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        self.setFont("Helvetica", 7)
        self.drawRightString(200*mm, 20*mm,
            "Page %d of %d" % (self._pageNumber, page_count))

def main():
    import sys
    import urllib2
    from cStringIO import StringIO
    from reportlab.platypus import SimpleDocTemplate, Image, Paragraph, PageBreak
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet

    #This is needed because ReportLab accepts the StringIO as a file-like object,
    #but doesn't accept urllib2.urlopen's return value
    def get_image(url):
        u = urllib2.urlopen(url)
        return StringIO(u.read())

    styles = getSampleStyleSheet()
    styleN = ParagraphStyle(styles['Normal'])

    # build doc

    if len(sys.argv) > 1:
        fn = sys.argv[1]
    else:
        fn = "filename.pdf"
    doc = SimpleDocTemplate(open(fn, "wb"))
    elements = [
        Paragraph("Hello,", styleN),
        Image(get_image("http://www.red-dove.com/images/rdclogo.gif")),
        PageBreak(),
        Paragraph("world!", styleN),
        Image(get_image("http://www.python.org/images/python-logo.gif")),
    ]
    doc.build(elements, canvasmaker=NumberedCanvas)

if __name__ == "__main__":
    main()
