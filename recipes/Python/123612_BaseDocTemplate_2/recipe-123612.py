"""
examples of reportlab document using
BaseDocTemplate with
2 PageTemplate (one and two columns)

"""
import os
from reportlab.platypus import BaseDocTemplate, Frame, Paragraph, NextPageTemplate, PageBreak, PageTemplate
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet


styles=getSampleStyleSheet()
Elements=[]

doc = BaseDocTemplate('basedoc.pdf',showBoundary=1)

def foot1(canvas,doc):
    canvas.saveState()
    canvas.setFont('Times-Roman',19)
    canvas.drawString(inch, 0.75 * inch, "Page %d" % doc.page)
    canvas.restoreState()
def foot2(canvas,doc):
    canvas.saveState()
    canvas.setFont('Times-Roman',9)
    canvas.drawString(inch, 0.75 * inch, "Page %d" % doc.page)
    canvas.restoreState()

#normal frame as for SimpleFlowDocument
frameT = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='normal')

#Two Columns
frame1 = Frame(doc.leftMargin, doc.bottomMargin, doc.width/2-6, doc.height, id='col1')
frame2 = Frame(doc.leftMargin+doc.width/2+6, doc.bottomMargin, doc.width/2-6,
               doc.height, id='col2')

Elements.append(Paragraph("Frame one column, "*500,styles['Normal']))
Elements.append(NextPageTemplate('TwoCol'))
Elements.append(PageBreak())
Elements.append(Paragraph("Frame two columns,  "*500,styles['Normal']))
Elements.append(NextPageTemplate('OneCol'))
Elements.append(PageBreak())
Elements.append(Paragraph("Une colonne",styles['Normal']))
doc.addPageTemplates([PageTemplate(id='OneCol',frames=frameT,onPage=foot1),
                      
                      PageTemplate(id='TwoCol',frames=[frame1,frame2],onPage=foot2),
                      ])
#start the construction of the pdf
doc.build(Elements)
# use external program xpdf to view the generated pdf
os.system("xpdf basedoc.pdf")
