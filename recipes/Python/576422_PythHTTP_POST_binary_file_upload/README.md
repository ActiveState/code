## Python HTTP POST binary file upload with pycurl  
Originally published: 2008-08-14 04:47:36  
Last updated: 2008-08-14 04:47:36  
Author: Robert Lujo  
  
There is a way to upload file with standard python libraries (urllib, httplib, ...) as explained at http://code.activestate.com/recipes/146306/. But that didn't worked for me for binary data. I didn't liked/tried solution explained at http://fabien.seisen.org/python/urllib2_multipart.html, so I tried with pycurl (http://pycurl.sourceforge.net/ wrapper for http://curl.haxx.se/libcurl/) because it is std. lib for php, and uploading the file is very simple (just add @<path-to-file> to post variable value). It was a little hard to find proper way because there is no such example or documentation. But I found it, and it is so simple ;)\n\nI supply django test application which receives file that is uploaded.