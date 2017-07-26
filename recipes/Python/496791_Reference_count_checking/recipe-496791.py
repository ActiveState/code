def getrc(defns,depth=1):
    '''get rc's for things in the space separated string defns'''
    from sys import getrefcount, _getframe
    f = _getframe(depth)
    G0 = f.f_globals
    L = f.f_locals
    if L is not G0:
        LL = [L]
        while 1:
            f = f.f_back
            G = f.f_globals
            L = f.f_locals
            if G is not G0 or G is L: break
            LL.append(L)
        L = {}
        for l in reversed(LL):
            L.update(l)
    else:
        L = L.copy()
    G0 = G0.copy()
    return ' '.join([str(getrefcount(eval(x,L,G0))-1) for x in defns.split()])

def checkrc(defns,rcv0):
    '''check rc's of things in defns against previously stored values
    return a string indicating those that have changed
    '''
    rcv1 = getrc(defns,2)
    return ' '.join(["%s %s-->%s" % (x,v,w) for x,v,w in zip(defns.split(),rcv0.split(),rcv1.split()) if v!=w])

def testStringWidth(incFontSize):
    '''example from the reportlab test set'''
    from _rl_accel import stringWidthU
    from reportlab.pdfbase.pdfmetrics import _py_stringWidth, getFont, registerFont, _fonts 
    from reportlab.pdfbase.ttfonts import TTFont
    ttfn = 'Luxi-Serif'
    t1fn = 'Times-Roman'
    registerFont(TTFont(ttfn, "luxiserif.ttf"))
    ttf = getFont(ttfn)
    t1f = getFont(t1fn)
    testCp1252 = 'copyright %s trademark %s registered %s ReportLab! Ol%s!' % (chr(169), chr(153),chr(174), chr(0xe9))
    enc='cp1252'
    senc = 'utf8'
    intern(senc)
    ts = 'ABCDEF\xce\x91\xce\xb2G'
    utext = 'ABCDEF\xce\x91\xce\xb2G'.decode('utf8')
    fontSize = 12
    defns="ttfn t1fn ttf t1f testCp1252 enc senc ts utext fontSize ttf.face ttf.face.charWidths ttf.face.defaultWidth t1f.widths t1f.encName t1f.substitutionFonts _fonts"
    rcv = getrc(defns)  #compute initial ref
    def tfunc(ts,fn,fontSize,enc):
        w1 = stringWidthU(ts,fn,fontSize,enc)
        w2 = _py_stringWidth(ts,fn,fontSize,enc)
        assert abs(w1-w2)<1e-10,"stringWidthU(%r,%r,%s,%r)-->%r != _py_stringWidth(...)-->%r" % (ts,fn,fontSize,enc,w1,w2)
    tfunc(testCp1252,t1fn,fontSize,enc)
    tfunc(ts,t1fn,fontSize,senc)
    tfunc(utext,t1fn,fontSize,senc)
    tfunc(ts,ttfn,fontSize,senc)
    tfunc(testCp1252,ttfn,fontSize,enc)
    tfunc(utext,ttfn,fontSize,senc)
    if incFontSize:
        z = fontSize    #simulate adding a reference to fontSize
    print checkrc(defns,rcv)

if __name__=='__main__':
    print 'should have no output',
    testStringWidth(0)
    print 'should change fontSize rc',
    testStringWidth(1)
