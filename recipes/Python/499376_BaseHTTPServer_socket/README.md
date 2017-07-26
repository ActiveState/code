## BaseHTTPServer with socket timeout

Originally published: 2007-01-14 10:00:48
Last updated: 2007-01-14 18:00:37
Author: Rogier Steehouder

BaseHTTPServer blocks while waiting for a connection. This means that a script will not respond to anything until it receives a network connection, which may never come. By adding a timeout to the listening socket, the script will regain control every so often.