## Use IIS/ASP or Apache/mod_python with the same application  
Originally published: 2003-09-27 15:13:10  
Last updated: 2003-09-27 15:13:10  
Author: Robert Brewer  
  
Both ASP and mod_python allow you to deploy web applications written in Python. This recipe allows you to push that decision down to your deployers, rather than your programmers. By abstracting the webserver, the same Python application can be deployed on either platform without rewriting.