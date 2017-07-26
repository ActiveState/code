from traceback import extract_stack

def makeDict(*args):
    strAllStack = str(extract_stack())
    intNumLevels = len( extract_stack() )
    intLevel = 0
    blnFinished = False
    while not blnFinished:
        strStack = str( extract_stack()[intLevel] )
        if strStack.find( "makeDict( ")>0:
            blnFinished = True
        intLevel += 1
        if intLevel >= intNumLevels:
            blnFinished = True
    strStartText = "= makeDict( "
    intLen = len( strStartText )
    intOpenParenLoc = strStack.find( strStartText )
    intCloseParenLoc = strStack.find(")", intOpenParenLoc )
    strArgs = strStack[ intOpenParenLoc+intLen : intCloseParenLoc ].strip()
    lstVarNames = strArgs.split(",")
    lstVarNames = [ s.strip() for s in lstVarNames ]   
    if len( lstVarNames ) == len( args ):
        tplArgs = map( None, lstVarNames, args )
        newDict = dict( tplArgs )
        return newDict
    else:
        print "Error.  makeDict Failed."
        return None
