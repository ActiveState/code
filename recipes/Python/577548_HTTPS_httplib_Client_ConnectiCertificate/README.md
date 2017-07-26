## HTTPS httplib Client Connection with Certificate Validation 
Originally published: 2011-01-18 18:30:45 
Last updated: 2011-01-18 18:30:45 
Author: Marcelo Fernández 
 
Despite httplib.HTTPSConnection lets the programmer specify the client's pair of certificates, it doesn't force the underlying SSL library to check the server certificate against the client keys (from the client point of view).\n\nThis class allows to force this check, to ensure the python client is connecting to the right server.