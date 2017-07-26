def getShortPathName(filepath):
    "Converts the given path into 8.3 (DOS) form equivalent."
    import win32api, os
    if filepath[-1] == "\\":
        filepath = filepath[:-1]
    tokens = os.path.normpath(filepath).split("\\")
    if len(tokens) == 1:
        return filepath
    ShortPath = tokens[0]
    for token in tokens[1:]:
        PartPath = "\\".join([ShortPath, token])
        Found = win32api.FindFiles(PartPath)
        if Found == []:
            raise WindowsError, 'The system cannot find the path specified: "%s"' % (PartPath)
        else:
            if Found[0][9] == "":
                ShortToken = token
            else:
                ShortToken = Found[0][9]
            ShortPath = ShortPath + "\\" + ShortToken
    return ShortPath
