#29-04-04
# v1.0.1
# E-mail fuzzyman AT atlantibots DOT org DOT uk (or michael AT foord DOT me DOT uk )
# Maintained at www.voidspace.org.uk/atlantibots/pythonutils.html
# Used by COnfigObj for storing config files with lists of values.

def listparse(inline, recursive = 1, comment = 1, retain = 0, lpstack = None, **keywargs):
    """Parses a line (a string) as a representation of a list. Can recursively parse nested lists. (List members can themselves be lists).
    List elements are stripped - and are returned as either lists or strings.

    This is useful for storing lists of information as text - for example in config files

    Listparse returns the list and trailing comments or None if the list is badly built.
    
    A valid comments exists after the end of the list (and any whitespace) and starts with a '#' or a ';'.
    Returned comment will include the initial '#' or a ';'.
    
    Commas delimit list elements.
    If the first non whitespace character in a list element is '[' then that element is treated as a list.

    Inside the list '[', ']', '"', "\" or '\' can be escaped with '\'
    (or indeed any other character - a single '\' will always be treated as escaping the character that follows)
    The leading '\' of escaped characters is *not* retained.....
    Any unquoted list elements must not have an unescaped ']' in them - except to terminate the current list.
    Escaping can be switched off by passing in a keyword argument 'escapechar' set to None.
    If you want to use literal '\' without escaping them - then you must switch escaping off.
    If you make sure every element of a list is contained within quotes - using the quot_elem function - this shouldn't be a problem).

    If retain is set to 1 (default is 0) any quotes around elements will be retained.
    This could be used to specify element types - e.g. if it has quotes it is a string. 
    So the function unquote can be used recursively to check if a list element is validly quoted.
    (and here you could implement other methods for unquoted elements - e.g. check for None or integer values etc...)
    *However* if an element is quoted - it must be correctly quoted, or the element will be invalid.
    The default is for quotes to be removed.

    If recursive is set to 0 (default is 1)
    then list elements will not be recursively parsed - an element containing another list will just
    be returned as a string.
    (meaning an unescaped and unquoted ']' will close the current list... and listparse will say you have a bad list).

    lpstack is used for recursion. Effectively it parses the current table and returns the rest of the line as well.

    If comment is set to 0 (default is 1)
    It causes listparse to return None if there is anything other than whitespace after a valid list.
    (I.e. comments are not allowed). In this case it will only return the list.
    """
    if keywargs.has_key('escapechar'):
        escapechar = keywargs['escapechar']         # either True or False
    else:
        escapechar = True
    outlist = []
    inline = inline.strip()
    if inline[0] != '[':
        return None
    inline = inline[1:].lstrip()
    found_end = 0
    thiselement = None
    escape = 0
    while inline:
        if thiselement == None:         # start of the element
            output = unquote(inline, 0, retain, escapechar=escapechar)          # partquote mode, retain quotes.......
            if output == None:
                return None
            if output != -1:            # element is quoted
                thiselement, inline = output
                inline = inline.lstrip()
                if not inline:
                    return None
                if inline[0] not in [',', ']']:     # only two valid ways to terminate an element
                    return None
                continue
                
        thischar = inline[0]
        inline = inline[1:]
        if escape:                      # the current character is escaped... whatever it may be
            thiselement =__add(thiselement, thischar)
            escape = 0
            continue
        elif thischar == '\\' and escapechar:
            escape = 1
#            thiselement = __add(thiselement, thischar)             # commenting this out means we no longer retain the initial '\' if quoting is on
            continue
        if recursive and not thiselement and thischar == '[':
            output = listparse('[' + inline, True, comment, retain, True, escapechar=escapechar)            # we have found a list element, herewith lies recursion...
            if not output:
                return None         # which is badly formed
            thiselement, inline = output
            inline = inline.lstrip()
            if not inline:
                return None
            if inline[0] not in [',', ']']:     # only two valid ways to terminate an element
                return None
            continue
        if thischar == ',':         # element terminated
            outlist.append(thiselement)
            thiselement = None
            inline = inline.lstrip()
            continue
        if thischar == ']':
            if thiselement != None:                     # trap empty lists
                outlist.append(thiselement)
            found_end = 1
            if lpstack:
                return outlist, inline
            break
        thiselement = __add(thiselement, thischar)
    if not found_end:
        return None
    inline = inline.strip()
    if inline and not comment:
        return None
    elif not comment:
        return outlist
    if inline and inline[0] not in ['#',';']:
        return None
    return outlist, inline
            
def __add(thiselement, char):
    """Shorthand for adding a character...."""
    if thiselement == None:
        return char
    return thiselement + char

def unquote(inline, fullquote = 1, retain = 0, **keywargs):
    """Given a line - if it's correctly quoted - it reurns the 'unquoted' value.
    If not quoted at all, it returns -1.
    If badly quoted, it returns None.
    
    line is stripped before starting.

    Any instances of '&mjf-quot;' found (from elem_quot) are turned back into '"'
    Any instances of '&mjf-lf;' found (from elem_quot) are turned back into '\n'
    
    Quotes can be escaped with a '\'.
    '\' (or any other character) can also be escaped with a '\'.
    No triple quotes though :-)
    (Escaping can be switched off by passing in the keyword argument 'escapechar' set to None
    If you want to use literal '\' without escaping them then you must turn escaping off).

    If fullquote is set to 0 (default is 1)
    then unquote will return the first correctly quoted part of the line *and* the rest of the line.
    If retain is set to 1 (default is 0)
    then unquote will retain the quote characters in the returned value."""
    if keywargs.has_key('escapechar'):
        escapechar = keywargs['escapechar']
    else:
        escapechar = True
    outline = ''
    quotes = ["'",'"']
    escape = 0
    index = 0
    quotechar = None
    inline = inline.strip()
    while index < len(inline):
        thischar = inline[index]
        index += 1
        if not quotechar and thischar not in quotes:
            return -1
        elif not quotechar:
            quotechar = thischar
            if retain:
                outline += thischar
            continue
        if escape:
            outline += thischar
            escape = 0
            continue
        if thischar in quotes:
            if thischar == quotechar:
                if retain:
                    outline += thischar
                if not fullquote:
                    return outline.replace('&mjf-quot;','\"').replace('&mjf-lf;','\n'), inline[index:]
                elif index == len(inline):
                    return outline.replace('&mjf-quot;','\"').replace('&mjf-lf;','\n')
                else:
                    return None
            else:
                outline += thischar
                continue
        if thischar == '\\' and escapechar:         # a continue here to *not* retain the escape character 
            escape = 1
            continue
        outline += thischar
    return None


def list_stringify(inlist):
    """Recursively rebuilds a list - making all the members strings...
    Useful before writing out lists.
    Used by makelist."""
    outlist = []
    for item in inlist:
        if not isinstance(item, list):
            if not isinstance(item, str):
                thisitem = str(item)
            else:
                thisitem = item
        else:
            thisitem = list_stringify(item)
        outlist.append(thisitem)
    return outlist


def makelist(inlist):
    """Given a list - will turn it into a string... suitable for writing out.
    (and then reparsing with listparse.)

    Uses list_stringify to make sure all elements are strings and
    elem_quote to decide the most appropriate quoting.

    (This means it adds quoting to every element and, where necessary, escapes
    '"' as '&mjf-quot;' and '\n' as '&mjf-lf;'........)."""
    inlist = list_stringify(inlist)
    outline = '['
    if not inlist:         # the member is set to None or is an empty list
        outline += ']'
    else:
        for item in inlist:
            if not isinstance(item, list):
                outline += elem_quote(item)
                outline += ', '
            else:
                outline += makelist(item)
                outline += ', '
        if outline[-2:] == ', ':
            outline = outline[:-2]
        outline += ']'
    return outline

def elem_quote(member):
    """Simple method to add the most appropriate quote to an element.
    Element is first converted to a string.
    If the element contains both \' and \" then \" is escaped as '&mjf-quot;'
    If the element contains \n it is escaped as '&mjf-lf;'
    Both are restored transparently by unquote.

    If you only have literal strings at this stage and will be parsing with escaping on -
    you might want to do a replace('\\', '\\\\') on the member too...
    """
#        member = str(member)                                            # since we now stringify everything - this is probably a redundant command
    if member.find("'") == -1:
        outline = "'" + member + "'"
    elif member.find('"') == -1:
        outline = '"' + member + '"'
    else:
        outline = '"' + member.replace('"','&mjf-quot;')+'"'
    return outline.replace('\n','&mjf-lf;')


# brief test stuff
if __name__ == '__main__':
    test ='["hello", \'hello2\']'
    test1 = """['hello',"hello again", and again,['hello',"hello again", and again,], and last of all]"""
    print listparse('[]')
    print test1
    print unquote('"hello baby", hello again', 0, 1)
    print listparse(test1)
    print listparse(test1,1,1,1)
    print listparse(test)
    test1 = test1 +'   # hello'
    print listparse(test1)
    print listparse(test1, 0)       # no recursion      - without recursion the list is very badly formed, so returns None
    print listparse(test1, 1, 0)    # the comment at the end causes listparse to return None here
