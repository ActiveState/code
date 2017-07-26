"""
recipe_custom_ps.py

Template with sample code creating for custom Postscript PS files.
Sample code is a business card based on Levenger's personalized
3x5 card.

Ghostscript provides easiest way to view PS output, but not essential.
Utilities included.

Download Ghostscript:
http://www.ghostscript.com/download/gsdnld.html
"""
__author__ = "Jack Trainor"
__date__ = "2015-12-09"

import sys
import os.path
import subprocess

######################################################################
""" 
String constants for business index card. 
"""
NAME = "John Doe"
ADDRESS = "123 Main Street"
CITY = "Anytown, USA  01234"
EMAIL = "johndoe123@gmail.com"
PHONE = "1.555.123.4567"
FAX = "1.555.123.4568"
CELL = "1.555.123.4569"

PHONE_FIELD = "Phone"
FAX_FIELD = "Fax"
CELL_FIELD = "Cell"

######################################################################
"""
Auxiliary utilities.

*** REPLACE WITH VALID PATHS ON YOUR MACHINE. ***
"""
PDF_VIEWER = r"C:\Program Files\Foxit Software\Foxit Reader\FoxitReader.exe"
GSC = r"C:\Program Files\gs\gs9.16\bin\gswin32c.exe"

def pdfview(path):
    """ Use PDF viewer to display pdf file. """
    if os.path.exists(PDF_VIEWER):
        subprocess.call([PDF_VIEWER, path])
    else:
        println("%s not installed." % PDF_VIEWER)
    
def gs_ps2pdf(input_ps, output_pdf):
    """ Use Ghostscript to convert PS file to PDF file """
    if os.path.exists(GSC):
        println("gs_ps2pdf: %s -> %s" % (input_ps, output_pdf))
        args =[GSC, 
            "-o", output_pdf, 
            "-sDEVICE=pdfwrite", 
            "-dPDFSETTINGS=/prepress", 
            "-dEmbedAllFonts=true", 
            "-dSubsetFonts=false", 
#            "-sFONTPATH=%s" % CUSTOM_FONTS  # for custom fonts if any
            "-dBATCH",
            "-dQUIET",
            "-c", ".setpdfwrite <</NeverEmbed [ ]>> setdistillerparams", 
            "-f"]
        args.append(input_ps)
        subprocess.call(args)
    else:
        println("%s not installed." % GSC)
        
def println(line):
    sys.stdout.write(line + "\n")

######################################################################
""" 
Postscript boilerplate for prolog and epilog of PS file.

Add your own Postscript procedures in prolog.
"""
PS_PROLOG = """%!PS-Adobe-2.0

%--------- Procedures ----------------
% Optimize without dict variables later, if at all
/rectPath               % stk: width height left top => -- 
{ /t exch def
  /l exch def
  /h exch def
  /w exch def
  
  newpath
  l t moveto
  w 0 rlineto
  0 h neg rlineto
  w neg 0 rlineto
  0 h rlineto
 } def

/centershow               % stk: y leftmargin rightmargin string => --
{ /s exch def
  /rm exch def
  /lm exch def
  /y exch def
  rm lm sub
  s stringwidth pop sub
  2 div
  lm add y moveto
  s show } def 

/rightshow               % stk: y rightmargin string => --
{ /s exch def
  /rm exch def
  /y exch def
  s stringwidth pop
  rm exch sub
  y moveto
  s show } def 

/gridPath               % stk: rows cols cellside left top => --
{ /top exch def
  /left exch def
  /cellside exch def
  /cols exch def
  /rows exch def

  /width cellside cols mul def
  /height cellside rows mul def
  
  newpath
  
  top /y exch def
  left /x exch def
  
  0 1 rows {
  x y moveto
  width 0 rlineto
  y cellside sub /y exch def
  } for
  
  top /y exch def
  left /x exch def
  
  0 1 cols {
  x y moveto
  0 height neg rlineto
  x cellside add /x exch def
  } for
} def

%---------- PS Card --------------------
"""

PS_EPILOG = """
%---------- Epilog ---------------------
% done with this page
showpage
"""

######################################################################
""" 
Constants for PS page and PS card 
"""
DPI = 72.0
def inches_to_dots(inches):
    return inches * DPI

PAGE_WIDTH = inches_to_dots(8.5)
PAGE_HEIGHT = inches_to_dots(11.0)

CARD_WIDTH = inches_to_dots(3.0)
CARD_HEIGHT = inches_to_dots(5.0)
CARD_LEFT = inches_to_dots(0.0)
CARD_TOP = CARD_HEIGHT 
CARD_MARGIN_X = inches_to_dots(.25)
CARD_MARGIN_Y = inches_to_dots(.25)

GRID_CELLSIZE = inches_to_dots(.25)
GRID_ROWS = 15
GRID_COLS = 10
GRID_LEFT = CARD_MARGIN_X
GRID_TOP = CARD_MARGIN_Y + GRID_ROWS * GRID_CELLSIZE

NAME_FONT = "Palatino-bold"
NAME_FONTSIZE = 13.0

FIELDS_FONT = "Palatino-medium"
FIELDS_FONTSIZE = 8.0

TITLE_HEIGHT = inches_to_dots(.25)
FIELDS_HEIGHT = inches_to_dots(.145)

TITLE_Y = CARD_TOP - CARD_MARGIN_Y + inches_to_dots(.07)
NAME_Y = TITLE_Y - TITLE_HEIGHT
ADDRESS_Y = NAME_Y - FIELDS_HEIGHT
CITY_Y = ADDRESS_Y - FIELDS_HEIGHT
EMAIL_Y = CITY_Y - FIELDS_HEIGHT

FIELD_NAME_X = inches_to_dots(2.0)
FIELD_VAL_X = inches_to_dots(2.05)

LINEWIDTH = 0.5

TEMPLATE_ROWS = 1
TEMPLATE_COLS = 1

TEMPLATE_MARGIN_BOTTOM = inches_to_dots(0.5)
TEMPLATE_MARGIN_LEFT = inches_to_dots(0.75)

######################################################################
""" 
Python wrappers for PS calls. Extend as necessary. Avoid using
raw Postscript in PsCard and PsPage calls.
"""
def setFont(font, fontsize):
    return "/%s findfont %f scalefont setfont" % (font, fontsize)

def rectPath( width, height, left, top):
    return "%.3f %.3f %.3f %.3f rectPath" % (width, height, left, top)

def gridPath(rows, cols, cellside, left, top):
    return "%d %d %.3f %.3f %.3f gridPath" % (rows, cols, cellside, left, top)

def leftShow(x, y, s):
    return "%.3f %.3f moveto (%s) show" % (x, y, s)

def rightShow(x, y, s):
    return "%.3f %.3f (%s) rightshow" % (y, x, s)

def linewidth(lw):
    return "%.3f setlinewidth" % lw

def setgray(percent):
    return " %.3f setgray" % percent

def translate(x, y):
    return "%.3f %.3f translate" % (x, y)

def gsave():
    return "gsave"

def grestore():
    return "grestore"

def draw_grid(lines, rows, cols, cellside, left, top):
    lines.append(gridPath(rows, cols, cellside, left, top))
    lines.append("stroke")

def draw_rect(lines, width, height, left, top):
    lines.append(rectPath(width, height, left, top))
    lines.append("stroke")

######################################################################
class PsRect(object):
    """ Uitility class for Poscript rect """
    def __init__(self, left, top, width, height):
        self.top = top
        self.left = left
        self.width = width
        self.height = height
        self.calc_fields()
        
    def calc_fields(self):
        self.bottom = self.top-self.height
        self.right = self.left+self.width
        self.center_x = self.left+self.width/2.0
        self.center_y = self.top-self.height/2.0
        
    def copy(self):
        return PsRect(self.left, self.top, self.width, self.height)
         
    def inset(self, inset_x, inset_y):
        self.left += inset_x
        self.top -= inset_y
        self.width -= 2*inset_y
        self.height -= 2*inset_y
        return self
        
    def to_ps(self, lw):  
        lines = []
        lines.append(linewidth(lw))
        draw_rect(lines, self.width, self.height, self.left, self.top)
        return "\n".join(lines)
 
######################################################################
class PsCard(object):
    """ PsCard supports Postscript description of a single card. """
    def __init__(self):
        pass
        
    def to_ps(self, lines):
        rect = PsRect(CARD_LEFT, CARD_TOP, CARD_WIDTH, CARD_HEIGHT)
        lines.append(rect.to_ps(LINEWIDTH))

        lines.append(setFont(NAME_FONT, NAME_FONTSIZE))
        lines.append(leftShow(CARD_MARGIN_X, NAME_Y, NAME))
          
        lines.append(setFont(FIELDS_FONT, FIELDS_FONTSIZE))
        lines.append(leftShow(CARD_MARGIN_X, ADDRESS_Y, ADDRESS))
        lines.append(leftShow(CARD_MARGIN_X, CITY_Y, CITY))
        lines.append(leftShow(CARD_MARGIN_X, EMAIL_Y, EMAIL))
         
        lines.append(rightShow(FIELD_NAME_X, ADDRESS_Y, PHONE_FIELD))
        lines.append(rightShow(FIELD_NAME_X, CITY_Y, FAX_FIELD))
        lines.append(rightShow(FIELD_NAME_X, EMAIL_Y, CELL_FIELD))
 
        lines.append(leftShow(FIELD_VAL_X, ADDRESS_Y, PHONE))
        lines.append(leftShow(FIELD_VAL_X, CITY_Y, FAX))
        lines.append(leftShow(FIELD_VAL_X, EMAIL_Y, CELL))
         
        lines.append(setgray(0.8))
        lines.append(linewidth(0.5))
        draw_grid(lines, GRID_ROWS, GRID_COLS, GRID_CELLSIZE, GRID_LEFT, GRID_TOP)

######################################################################
class PsPage(object):
    """ Supports Postscript description of a single page. """
    def __init__(self):
        self.page_ps = ""
        self.page_path = ""
        self.card = PsCard()        
        
    def cards_to_ps(self, lines):  
        """ Can tile cards to page if TEMPLATE_ROWS and TEMPLATE_COLS > 1 """
        for row in range(0, TEMPLATE_ROWS):
            for col in range(0, TEMPLATE_COLS):
                x = TEMPLATE_MARGIN_LEFT + col * CARD_WIDTH
                y = TEMPLATE_MARGIN_BOTTOM + row * CARD_HEIGHT
                self.card_to_ps(lines, x, y)
    
    def card_to_ps(self, lines, x, y):  
        lines.append(gsave())
        lines.append(translate(x, y))
        self.card.to_ps(lines)
        lines.append(grestore())
        lines.append("\n")
        
    def to_ps(self):
        lines = []
        lines.append(PS_PROLOG)
        self.cards_to_ps(lines)
        lines.append(PS_EPILOG)
        return "\n".join(lines)
    
######################################################################
OUTPUT_DIR = "C:\\"
PSCARD_PS = "ps_indexcard.ps"
PSCARD_PDF = "ps_indexcard.pdf"

def test_page():
    page = PsPage()
    ps = page.to_ps()
    ps_path = os.path.join(OUTPUT_DIR, PSCARD_PS)
    with open(ps_path, "w") as out:
        out.write(ps)
    pdf_path = os.path.join(OUTPUT_DIR, PSCARD_PDF)   
    gs_ps2pdf(ps_path, pdf_path)
    pdfview(pdf_path)
    
######################################################################
if __name__ == "__main__":
    test_page()
