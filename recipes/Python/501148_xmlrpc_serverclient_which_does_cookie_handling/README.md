## xmlrpc server/client which does cookie handling and supports basic authentication  
Originally published: 2007-01-23 10:51:39  
Last updated: 2007-01-23 10:51:39  
Author: Vaibhav Bhatia  
  
xmlrpc server client which do the following:
* client sends a request with basic authentication
* server on successful authentication sends response back and also sends cookies with authentication id
* these cookies are saved by client and then used for authentication on any subsequent requests