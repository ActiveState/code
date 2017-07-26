#!/usr/bin/python

import cgi

def cgiFieldStorageToDict( fieldStorage ):
   """Get a plain dictionary, rather than the '.value' system used by the cgi module."""
   params = {}
   for key in fieldStorage.keys():
      params[ key ] = fieldStorage[ key ].value
   return params

if __name__ == "__main__":
   dict = cgiFieldStorageToDict( cgi.FieldStorage() )
   print "Content-Type: text/plain"
   print
   print dict
