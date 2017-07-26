## Enable xmlrpclib to maintain a JSP session  
Originally published: 2002-11-10 08:46:45  
Last updated: 2002-11-10 08:46:45  
Author: Danny Yoo  
  
This extension to xmlrpclib allows us to maintain a session with a JSP server, so that there appears to be a stateful session.  It tries to maintain the JSESSIONID call between calls to the server.