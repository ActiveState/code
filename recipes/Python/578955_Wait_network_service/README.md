###Wait for network service to appear

Originally published: 2014-11-06 07:29:11
Last updated: 2014-11-06 07:29:12
Author: Mohammad Taha Jahangir

This script allows you to wait until specified port is opened on remote server. This can be useful in automation jobs - restarting server, wake on lan etc. It can also be used for monitoring distant service/site.\n\nThe main problem that this script solves is that you need to handle two different timeouts when opening probing socket, and it is not described in python documentation. See http://bugs.python.org/issue5293 for more information.