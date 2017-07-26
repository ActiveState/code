## Display Servers.  
Originally published: 2004-09-19 22:29:12  
Last updated: 2004-09-19 22:29:12  
Author: Patrick Finnegan  
  
Display running servers on WAS node.

Called from WSAdmin bat file.

@echo off

echo ###################################################
echo # Display WAS application servers on %COMPUTERNAME%
echo ###################################################

command.com /c

call wsadmin -username cccccc^
             -password cccccc^
             -f d:\scripts\websphere\JACL\displayServers.tcl