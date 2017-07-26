def getimporter():
    ''' Placing this inside a module X, return a 7-tuple representing
        the module that is importing X:

        ( modulename,  frame, filepath, lineno, name, codetext, somenumber )

        The items starting from the 2nd one are the 6-tuple frame info.
        For example, when a file 'importer.py' imports a module 'imported.py'
        in which this function "getimporter" is placed, getimporter will
        report:

        ('importer',
        <frame object at 0x014C7A80>, 'E:\\py\\src\\importer.py',
        2, 'importer', ['import imported\n'], 0)        

        This function is useful when users intend to do different things
        with a module X according to the properties/attributes of a module
        that is importing X. That is, an 'importer-specific 
        module initialization'.
        
        Usage:
        ------
        
        importer = getimporter()
        if importer[0] == 'mytools': (do something)
        else: (do something else)

        or, it might be helpful in avoiding recursive importing:

        importer = getimporter()
        if importer[0] == 'mytools': import some module
        else: import another module
        
        How it works:
        -------------

        The inspect.stack() returns a list of 6-tuples for the execution
        stack. Each 6-tuple is a frame info:

        (frame, filepath, lineno, name, codetext, somenumber)

        When an inspect.stack() is placed in a module X, and X is
        imported by Y, then one of the 6-tuples will look like:        
        
        info= (<frame object at 0x00BA04A0>, 'C:\\pan\\py\\src\\Y.py',
        2, '?', ['import X\n'], 0)

        in which the 1st item of the info[4] is a string starting with
        either 'import X' or 'from X' or ' import pantools.X' or
        ' from pantools.X'. This will serve as the criteria for finding Y.
    '''

    # First find the name of module containing this (getimporter)
    
    frame, path, lineno, name, codetext, somenumber= inspect.stack()[1]
    module =  os.path.split(path)[1].split('.')[0]   # get the module name only
    
    # Then get the calling stack       
    for frame, file, lineno, name, codetext, somenumber in inspect.stack():
        codetexts = codetext[0].split() # The first will be either 'from' or 'import'

        # Possibilities:
        #
        # import X
        # form   X import blah
        # import tools.X
        # from   tools.X import blah
        
        if codetexts[0] in ('from', 'import') and \
           codetexts[1].split('.')[-1] == module:
            name = os.path.split(file)[1].split('.')[0]
            return name, frame, file, lineno, name, codetext, somenumber
    return (None, )
