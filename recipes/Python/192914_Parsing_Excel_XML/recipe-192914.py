import sys
from xml.sax import saxutils
from xml.sax import parse

class ExcelHandler(saxutils.DefaultHandler):
    def __init__(self):
        self.chars=[]
        self.cells=[]
        self.rows=[]
        self.tables=[]
        
    def characters(self, content):
        self.chars.append(content)

    def startElement(self, name, atts):
        if name=="Cell":
            self.chars=[]
        elif name=="Row":
            self.cells=[]
        elif name=="Table":
            self.rows=[]
    
    def endElement(self, name):
        if name=="Cell":
            self.cells.append(''.join(self.chars))
        elif name=="Row":
            self.rows.append(self.cells)
        elif name=="Table":
            self.tables.append(self.rows)
    
excelHandler=ExcelHandler()
parse(sys.argv[1], excelHandler)
print excelHandler.tables
