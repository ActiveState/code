## WSAdmin - Install Server.  
Originally published: 2004-08-31 22:01:23  
Last updated: 2004-08-31 22:01:23  
Author: Patrick Finnegan  
  
WSAdmin JACL script to install and set properties for an application server running under WAS 5.1 base installation.

Called by a Windows bat file.

@echo off

set server=YourServer

echo ###################################################
echo # Install %server% on %COMPUTERNAME%
echo ###################################################

command.com /c

call wsadmin -username yourname^
             -password yourpassword^
             -f C:\scripts\websphere\JACL\installServer.tcl %server%
