## IP address conversion functions with the builtin socket module

Originally published: 2001-08-14 09:14:39
Last updated: 2001-08-14 09:14:39
Author: Alex Martelli

Convert dotted-quad IP addresses to long integer and back, get network and host portions from an IP address, all nice and fast thanks to the builtin socket module (with a little help from the builtin struct module, too).