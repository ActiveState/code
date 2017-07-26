###Display Servers.

Originally published: 2004-09-19 22:29:12
Last updated: 2004-09-19 22:29:12
Author: Patrick Finnegan

Display running servers on WAS node.\n\nCalled from WSAdmin bat file.\n\n@echo off\n\necho ###################################################\necho # Display WAS application servers on %COMPUTERNAME%\necho ###################################################\n\ncommand.com /c\n\ncall wsadmin -username cccccc^\n             -password cccccc^\n             -f d:\\scripts\\websphere\\JACL\\displayServers.tcl