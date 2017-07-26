#!/usr/bin/python

# Create an m3u playlist file on the fly
# Use the query string in the URI to create the file name in the playlist
# This python script's extension is .m3u instead of .py, to fool the browser into opening an MP3 player
# Despite its extension, the top line in this script makes it executable as a python script

# Davide Andrea, KGNU 2/24/06

import cgi

AudioPath = 'http://kgnu.net/audio/%s_%s.mp3'


def Main():
#------------------
# Main procedure
  print "Content-type: text\n"	               # Note that its not text/html, as it would be for a web page
  uriQuery = cgi.FieldStorage()                # Get the query string from the URI
  showCode = uriQuery.getfirst('show','')      # From it, get the show name
  recDate = uriQuery.getfirst('date','')       #  and the date
  filePath = (AudioPath % (showCode, recDate)) # Assemble the file name and path
  print filePath                               # This is the content of the "file" served, that the MP3 player will see


#------------------
# Main
Main()					# Do the main procedure
