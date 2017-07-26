###Stoppable HTTP server

Originally published: 2004-11-17 15:08:24
Last updated: 2004-11-17 15:08:24
Author: wurst2 

Starting a SimpleHTTPServer instance in a separate thread makes it run forever. To solve this problem the server is augmented with a QUIT command. If sent it makes the server stop serving requests.