###get the IP address associated with a network interface (linux only)

Originally published: 2005-08-11 13:30:18
Last updated: 2005-08-11 13:30:18
Author: paul cannon

Uses the Linux SIOCGIFADDR ioctl to find the IP address associated with a network interface, given the name of that interface, e.g. "eth0".  The address is returned as a string containing a dotted quad.