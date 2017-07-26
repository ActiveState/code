## WSAdmin - Install Virtual Host.  
Originally published: 2004-08-31 22:34:52  
Last updated: 2004-08-31 22:34:52  
Author: Patrick Finnegan  
  
Install a virtual host on WebSphere 5.1 base installation.

Called from a Windows bat file.

@echo off

set vhName=your_host
set vh=www.yoursite.com

echo ###################################################
echo # Install %vhName% on %COMPUTERNAME%
echo ###################################################

command.com /c

call wsadmin -username userid^
             -password password^
             -f C:\scripts\websphere\JACL\installVirtualHost.tcl %vhName% %vh%