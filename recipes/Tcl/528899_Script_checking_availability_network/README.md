###Script checking availability of network servers

Originally published: 2007-08-27 01:58:17
Last updated: 2007-08-27 23:57:08
Author: Alex Khokhlov

Script checking availability of network servers\nIf the server is not accessible, starts action\nThe necessary data are read from a text file\n\nThe file of the data contains lines of a kind:\n\nsmtp_server:25:any_executed_program:my_smtp_server\nhttpd_daemon:80:ps:corp_web_server