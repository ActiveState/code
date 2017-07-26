## urllib2 for actions depending on http response codesOriginally published: 2004-02-07 13:34:32 
Last updated: 2004-02-07 13:34:32 
Author: Lee Harr 
 
I wanted to touch a particular web page (in order to open/close a database connection inside of Zope) so I came up with this module which uses urllib2 to make the web connection\n\nI was not sure what a 'realm' was, so first I made the HTTPRealmFinder to find out what the realm is.\n\nThe HTTPinger calls my required page and acts according to the http return code.