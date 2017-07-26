from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._codes = []
    def showPage(self):
        self._codes.append({'code': self._code, 'stack': self._codeStack})
        self._startPage()
    def save(self):
        """add page info to each page (page x of y)"""
        # reset page counter 
        self._pageNumber = 0
        for code in self._codes:
            # recall saved page
            self._code = code['code']
            self._codeStack = code['stack']
            self.setFont("Helvetica", 7)
            self.drawRightString(200*mm, 20*mm,
                "page %(this)i of %(total)i" % {
                   'this': self._pageNumber+1,
                   'total': len(self._codes),
                }
            )
            canvas.Canvas.showPage(self)

# build doc
doc = SimpleDocTemplate("filename.pdf")
... # add your report definition here
doc.build(elements, canvasmaker=NumberedCanvas)
