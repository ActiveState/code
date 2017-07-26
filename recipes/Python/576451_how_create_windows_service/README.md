## how to create a windows service in python

Originally published: 2008-08-26 01:32:47
Last updated: 2008-08-26 01:32:47
Author: alexander baker

The following code snippet shows you have to create a windows service from a python script. The most important thing here is the username and password, if you ignore supplying these the server will never start and you will get a message saying that the service has not responded in time, this is a red herring. The default account that the pythonservice wrapper uses is not permissioned to run the service. 