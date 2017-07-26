## Traceback that does'nt output on sys.stderrOriginally published: 2001-06-25 04:25:48 
Last updated: 2001-06-25 04:25:48 
Author: Dirk Holtwick 
 
For CGI programmers it's important to display tracebacks in the HTML pages to debug their scripts, but the usual functions in the modules cgi and traceback print to sys.sterr. So this small programm returns the traceback as a string an can even add entities for HTML.