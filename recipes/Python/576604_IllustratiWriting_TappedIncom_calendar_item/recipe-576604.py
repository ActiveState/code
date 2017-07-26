from glob import glob
from re import compile
from datetime import datetime, timedelta
import webbrowser
from string import join
from urllib import quote, quote_plus
from win32api import GetTempPath
from tempfile import mkstemp
from os import remove

## thanks to Dalziel(?)
## at
## http://blog.slaven.net.au/archives/2006/08/17/posting-to-windows-live-writer-from-feeddemon/
## for a big hint

HTMLpatt = compile ( r'''<a href="([^"]+)">\[([^]]+)\]\s*([^(]+)\s*\(\s*([0-9]+)''' )

folder = GetTempPath ( )

maxFileNumber = '0000'
for fileName in glob ( r'''%s\*.post''' % folder ) :
	maxFileNumber = max ( maxFileNumber, fileName [ -9 : -5 ] )
	
postFileName = '%s%s.post' % ( fileName [ : -9 ], maxFileNumber, )

postFile = open ( postFileName )

HTMLline = postFile . readline ( ) . strip ( )
postFile . readline ( )
description = postFile . readline ( ) . strip ( )

postFile . close ( )

mat = HTMLpatt . search ( HTMLline )
URL = mat . groups ( ) [ 0 ]
rawDate = mat . groups ( ) [ 1 ]
title = mat . groups ( ) [ 2 ]
duration = int ( mat . groups ( ) [ 3 ] )

dateAndTime = datetime . strptime ( rawDate [ : -4 ], '%b %d, %Y, %I:%M %p' ) 
dateAndTime = dateAndTime - timedelta ( hours = 4 ) ## needs work here!
endDateAndTime = dateAndTime + timedelta ( hours = duration )

URLparts = {
	'action' : 'TEMPLATE',
	'text' : 'TappedIn: %s' % title,
	'location' : 'on line',
	'details' : '%s\n\n%s' % ( description, URL, ),
	'dates' : '%s/%s' % ( dateAndTime . strftime ( '%Y%m%dT%H%M00Z' ), endDateAndTime . strftime ( '%Y%m%dT%H%M00Z' ), ),
	'trp' : 'false',
	'sprop' : 'TappedIn: %s' % title,
	'sprop' : URL,
}

parameters = [ ]
for URLpart in URLparts :
	parameters . append ( '&%s=%s' % ( URLpart, quote ( URLparts [ URLpart ] ), ) )
	
GoogleURLtemplate = r'''<a href="http://www.google.com/calendar/event?%s"><img src="http://www.google.com/calendar/images/ext/gc_button2.gif"></a>'''

ignore, GoogleOfferHTMLFilename = mkstemp ( '.htm' )
GoogleOfferHTML = file ( GoogleOfferHTMLFilename, 'w' )
GoogleOfferHTML . write ( GoogleURLtemplate % join ( parameters, '' ) )
GoogleOfferHTML . close ( )

webbrowser . open ( GoogleOfferHTMLFilename )

remove ( GoogleOfferHTMLFilename )
