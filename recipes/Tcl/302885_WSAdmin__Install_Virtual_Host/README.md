## WSAdmin - Install Virtual Host. 
Originally published: 2004-08-31 22:34:52 
Last updated: 2004-08-31 22:34:52 
Author: Patrick Finnegan 
 
Install a virtual host on WebSphere 5.1 base installation.\n\nCalled from a Windows bat file.\n\n@echo off\n\nset vhName=your_host\nset vh=www.yoursite.com\n\necho ###################################################\necho # Install %vhName% on %COMPUTERNAME%\necho ###################################################\n\ncommand.com /c\n\ncall wsadmin -username userid^\n             -password password^\n             -f C:\\scripts\\websphere\\JACL\\installVirtualHost.tcl %vhName% %vh%