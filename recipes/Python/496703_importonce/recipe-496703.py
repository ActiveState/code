def import_once(modulenames, silent=1):
##    import_once
##    Fedmich   Last modified: 3:38 PM 5/15/2006
##    version 1.1
##    Usage:
##    import_once('os')
##    import_once( ["os", 'sys'] )
    
    if type(modulenames) is list:
        pass
    elif type(modulenames) is tuple:
        pass
    else:
        modulenames = [modulenames]

    imported = 0
    for modulename in modulenames:
        print modulename
        if globals().has_key(modulename):
            if not silent:  print """Already imported module "%s"...""" % modulename
            imported +=1
        else:
            try:
                if not silent:  print """%s is not yet imported so import it now...""" % modulename
                globals()[modulename] = __import__(modulename, globals(), locals(), [])
                imported += 1
            except:
                if not silent:  print """Error while importing "%s"...""" % modulename

    return (imported == len(modulenames) )  #return true if every modules are successfuly imported

print import_once( ("os", "sys") )

import_once( "sys")
import_once("oyster")
import_once("psyco", silent=0)  #silent is used for debugging...

print os
print sys
print os.path.basename(r"c:\WINNT")
