## Exposing a Pyro remote object as a web service via XMLRPC with CherryPy 
Originally published: 2004-11-23 02:50:16 
Last updated: 2004-11-23 02:50:16 
Author: gian paolo ciceri 
 
This recipe shows how to build an xmlrpc multithread server that exposes a Pyro remote object as a web service. Be careful to the remote object state: two different ways (a global and a thread local) are shown.