#!/usr/bin/python -u
# 2004/10/15
#v1.0.0 

# webcounter.py
# A very simple webcounter.

# Copyright Michael Foord
# You are free to modify, use and relicense this code.
# No warranty express or implied for the accuracy, fitness to purpose or otherwise for this code....
# Use at your own risk !!!

# For information about bugfixes, updates and support, please join the Pythonutils mailing list.
# http://voidspace.xennos.com/mailman/listinfo/pythonutils_voidspace.xennos.com
# Comments, suggestions and bug reports welcome.
# Scripts maintained at www.voidspace.org.uk/atlantibots/pythonutils.html
# E-mail michael AT foord DOT me DOT uk

"""
This saves a count of accesses and returns a single line of javascript.
This writes the number into the webpage.

Insert the following entry into your page :
<script language=JavaScript src="http://www.voidspace.xennos.com/cgi-bin/webcounter.py?site=SITENAME"></script>

That will use the version hosted on my server.
Replace SITENAME with something that is likely to be unique.
"""


########################################################################
# imports

import os
import cgi
import time

try:
    import cgitb
    cgitb.enable()
except:
    sys.stderr = sys.stdout

############################################
# values

sitedir = 'webcounter/'             # directory to store counter files  
logfile = '.counter'                # each site will have it's own counter file. The full path is sitedir + sitename + logfile

# timeformat is used by strftime in the time module
# It defines how the date is displayed.
# set to '' to omit.
# Only edit if you understand strftime. 
timeformat = "%d %B, %Y."

serverline = 'Content-type: application/x-javascript\n'        # header to send for stats output, just text so far

# This is the actual Javascript returned
thescript = 'document.writeln("%s");'
line1 = "%s visitors"
line2 = "%s visitors since<br />%s"
errormsg = 'Counter Error - No site specified.'

######################################################################
        
def main():
    theform = cgi.FieldStorage()                        # get the form
    try:
        thesite = theform['site'].value
    except KeyError:
        thesite = ''
    counterfile = sitedir+thesite+logfile
    if not os.path.isdir(sitedir):
        os.makedirs(sitedir)

    if not thesite:
        themsg = thescript % errormsg
    else:
        if os.path.isfile(counterfile):  
            filehandle = open(counterfile, 'r')
            counterdata = filehandle.readlines()
            filehandle.close()
            thedate = counterdata[1]
            thecount = counterdata[0]
        else:
            if timeformat:
                thedate = time.strftime(timeformat)
            else:
                thedate = ''
            thecount = "0"
        thecount = str(int(thecount)+1)
        filehandle = open(counterfile, 'w')
        filehandle.write(thecount+'\n')
        filehandle.write(thedate)
        filehandle.close()

        if timeformat:
            msgline = line2 % (thecount, thedate)
        else:
            msgline = line1 % thecount
        themsg = thescript % msgline

    print serverline
    print themsg

########################################################################
if __name__ =='__main__':
    main()

"""
TODO


ISSUES


CHANGELOG

2004/10/15      Version 1.0.0
A very simple CGI.
"""
