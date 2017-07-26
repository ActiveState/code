import re
import keyword

###Following are some crude regexes which I use to tokenise a text object comprising python code
multiline_pat = "(\'\'\'|\"\"\")"+r"(.|\n)*?\1"
singleline_pat = "(\'|\")"+r".*?\1"
kw_pat = r"\b("+"|".join(keyword.kwlist)+r")\b"
number_pat = r"\b\d+\b"
def_pat = r"((?<=def )\w+)|((?<=class )\w+)"
comment_pat = r"#.*(\n|$)"

###Define some colors for each token type
kwcolor = RGB( 255, 0, 0 )
numberColor = RGB( 128, 50, 0)
defColor = RGB(0,0,255)
StrColor = RGB(125,125,0) 
CommentColor = RGB(128,128,128)
MultiStrColor = RGB(0,255,0)

def RGB( nRed, nGreen, nBlue ):
    """Return an integer which repsents a color.
    The color is specified in RGB notation.
    Each of nRed, nGreen and nBlue must be a number from 0 to 255.
    """
    return (int( nRed ) & 255) << 16 | (int( nGreen ) & 255) << 8 | (int( nBlue ) & 255) 

def HighlightPython():
    """
    Main function for highlighting python code in a document. Must be called 'in process'.
    """
    ctx = XSCRIPTCONTEXT
    doc = ctx.getDocument()
    HighlightAll(doc)

def _highlight(pat, data, csr, color):
    """
    Does the actual coloring of text
    
    @param pat: a regex to find patterns to highlight
    @param data: the source text to use, a string
    @param csr: a OOo TextCursor instance
    @param color: an integer representing a color. use the RGB() function above to calculate
    """
    pos=0
    csr.gotoStart(False)
    print "pattern:", pat
    for match in re.finditer(pat, data):
        start, end = match.span()
        print "match:", data[start:end]
        diff = start-pos
        csr.goRight(diff, False)
        csr.goRight(end-start,True)
        csr.CharColor = color
        pos=end
    
def ColourTextBox(txt):
    """
    Highlights a single TextShape item
    """
    data = txt.String
    csr = txt.createTextCursor()
    _highlight(kw_pat, data, csr, kwcolor)
    _highlight(number_pat, data, csr, numberColor)
    _highlight(def_pat, data, csr, defColor )
    _highlight(singleline_pat, data, csr, StrColor)
    _highlight(comment_pat, data, csr, CommentColor )
    _highlight(multiline_pat, data, csr, MultiStrColor )
    
    
def RemoteGetDoc():
    """
    Retrieve the document instance when accessing OOo 'out of process', using uno over a socket.
    """
    import uno
    localContext = uno.getComponentContext()
    resolver = localContext.ServiceManager.createInstanceWithContext(
                    "com.sun.star.bridge.UnoUrlResolver", localContext )
    ctx = resolver.resolve( "uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext" )
    smgr = ctx.ServiceManager
    desktop = smgr.createInstanceWithContext( "com.sun.star.frame.Desktop",ctx)
    doc = desktop.getCurrentComponent()
    return doc
    
def HighlightAll(doc):
    """
    Apply syntax highlighting to all TextShapes in the document which have the "code"
    graphic style applied to them
    """
    styles = doc.StyleFamilies.getByName(u"graphics")
    code = styles.getByName(u"code")
    pages = doc.DrawPages
    count = pages.getCount()
    for idx in xrange(count):
        page = pages.getByIndex(idx)
        count = page.getCount()
        for item_idx in xrange(count):
            item = page.getByIndex(item_idx)
            if 'com.sun.star.drawing.TextShape' in item.SupportedServiceNames:
                style = item.Style
                if style==code:
                    ColourTextBox(item)
    
g_exportedScripts = (HighlightPython,)
    
if __name__=="__main__":
    #Script testing is easiest using remote uno over a socket
    doc = RemoteGetDoc()
    HighlightAll(doc)
    
    
