import os

def catenateFilesFactory(isTextFiles=True, isClearTgt=True, isCreateTgt=True):
    """return a catenateFiles function parameterized by the factory arguments.
    isTextFiles:    Catenate text files.  If the last line of a non-empty file 
                    is not terminated by an EOL, append an EOL to it.
    isClearTgt      If the target file already exists, clear its original 
                    contents before appending the source files.
    isCreateTgt     If the target file does not already exist, and this
                    parameter is True, create the target file; otherwise raise 
                    an IOError.
    """
    eol = os.linesep
    lenEol = len(eol)

    def catenateFiles(tgtFile, *srcFiles):
        isTgtAppendEol = False
        if os.path.isfile(tgtFile):
            if isClearTgt:
                tgt = open(tgtFile, 'wb')
                tgt.close()
            elif isTextFiles:
                tgt = open(tgtFile, 'rb')
                data = tgt.read()
                tgt.close()
                if len(data) and (len(data) < lenEol or data[-lenEol:] != eol):
                    isTgtAppendEol = True
        elif not isCreateTgt:
            raise IOError, "catenateFiles target file '%s' not found" % ( 
                    tgtFile)
        tgt = open(tgtFile, 'ab')
        if isTgtAppendEol:
            tgt.write(eol)
        for srcFile in srcFiles:
            src = open(srcFile, 'rb')
            data = src.read()
            src.close()
            tgt.write(data)
            if (isTextFiles and len(data) and
                    (len(data) < lenEol or data[-lenEol:] != eol)):
                tgt.write(eol)
        tgt.close()
        return            

    # Support reflection and doc string.
    catenateFiles.isTextFiles = isTextFiles
    catenateFiles.isClearTgt = isClearTgt
    catenateFiles.isCreateTgt = isCreateTgt
    
    if isTextFiles:
        docFileType = "text"
    else:
        docFileType = "binary"
    if isCreateTgt:
        docCreate = "Create tgtFile if it does not already exist."
    else:
        docCreate = "Require that tgtFile already exists."
    if isClearTgt:
        docClear = "replace"
    else:
        docClear = "append to"
    catenateFiles.__doc__ = """Catenate %s srcFiles to %s the tgtFile.
    %s
    All of the srcFiles must exist; otherwise raise an IOError.
    """ % (docFileType, docClear, docCreate)

    return catenateFiles
