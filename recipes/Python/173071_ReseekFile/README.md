## ReseekFile  
Originally published: 2003-01-09 16:09:13  
Last updated: 2003-01-09 16:09:13  
Author: Andrew Dalke  
  
Wrap a file handle to allow seeks back to the beginning

Sometimes data coming from a socket or other input file handle isn't
what it was supposed to be.  For example, suppose you are reading from
a buggy server which is supposed to return an XML stream but can also
return an unformatted error message.  (This often happens because the
server doesn't handle incorrect input very well.)

A ReseekFile helps solve this problem.  It is a wrapper to the
original input stream but provides a buffer.  Read requests to the
ReseekFile get forwarded to the input stream, appended to a buffer,
then returned to the caller.  The buffer contains all the data read so
far.

The ReseekFile can be told to reseek to the start position.  The next
read request will come from the buffer, until the buffer has been
read, in which case it gets the data from the input stream.  This
newly read data is also appended to the buffer.

When buffering is no longer needed, use the 'nobuffer()' method.  This
tells the ReseekFile that once it has read from the buffer it should
throw the buffer away.  After nobuffer is called, the behaviour of
'seek' is no longer defined.

For example, suppose you have the server as above which either
gives an error message is of the form:

&nbsp;&nbsp;ERROR: cannot do that

or an XML data stream, starting with "<?xml".

&nbsp;&nbsp;  infile = urllib2.urlopen("http://somewhere/")
&nbsp;&nbsp;  infile = ReseekFile.ReseekFile(infile)
&nbsp;&nbsp;  s = infile.readline()
&nbsp;&nbsp;  if s.startswith("ERROR:"):
&nbsp;&nbsp;&nbsp;&nbsp;      raise Exception(s[:-1])
&nbsp;&nbsp;  infile.seek(0)
&nbsp;&nbsp;  infile.nobuffer()   # Don't buffer the data
&nbsp;&nbsp;   ... process the XML from infile ...


This module also implements 'prepare_input_source(source)' modeled on
xml.sax.saxutils.prepare_input_source.  This opens a URL and if the
input stream is not already seekable, wraps it in a ReseekFile.