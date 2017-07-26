###Wait for network service to appear

Originally published: 2009-02-20 09:04:48
Last updated: 2009-02-20 14:04:11
Author: anatoly techtonik

This script allows you to wait until specified port is opened on remote server. This can be useful in automation jobs - restarting server, wake on lan etc. It can also be used for monitoring distant service/site.\n\nThe main problem that this script solves is that you need to handle two different timeouts when opening probing socket, and it is not described in python documentation. See http://bugs.python.org/issue5293 for more information.