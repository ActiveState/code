from StringIO import StringIO
from traceback import print_exc

try:
   raise Exception

except Exception, e:
    f=StringIO()      # this creates a file object
    print_exc(file=f)
    error_mess = f.getvalue().splitlines()
    print "Damn... Exception Occurred :\n"
    for line in error_mess:
        print line
    dummy = raw_input('Hit Enter........ ') 
