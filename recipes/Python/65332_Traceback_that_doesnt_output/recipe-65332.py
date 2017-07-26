def ErrorMsg(escape=0):
    """
    returns: string
    
    simualtes the traceback output and if argemument
    <escape> set to 1 (true) the string will be
    converted to fit into html documents without problems.    
    """
    import traceback, sys, string
    
    type=None
    value=None
    tb=None
    limit=None
    type, value, tb = sys.exc_info()
    body = "Traceback (innermost last):\n"
    list = traceback.format_tb(tb, limit) +            traceback.format_exception_only(type, value)
    body = body + "%-20s %s" % (
        string.join(list[:-1], ""),
        list[-1],
        )
    if escape:
        import cgi
        body = cgi.escape(body)
    return body

if __name__=="__main__":
    try:
        1/0
    except:
        print ErrorMsg()
 
