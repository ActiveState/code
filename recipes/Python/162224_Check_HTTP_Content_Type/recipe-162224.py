import urllib
from types import *
def iscontenttype(URLorFile,contentType='text'):
    """
    Return true or false (1 or 0) based on HTTP Content-Type.
    Accepts either a url (string) or a "urllib.urlopen" file.
    
    Defaults to 'text' type.
    Only looks at start of content-type, so you can be as vague or precise
    as you want.
    For example, 'image' will match 'image/gif' or 'image/jpg'.
    """
    result = 1
    try:
        if type(URLorFile) == StringType:
            file=urllib.urlopen(URLorFile)
        else:
            file = URLorFile

        testType=file.info().getheader("Content-Type")
        if testType and testType.find(contentType) == 0:
            result=1
        else:
            result=0
        if type(URLorFile) == StringType:
            file.close()
        return result
    except:
        return 0
