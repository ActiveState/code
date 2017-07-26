## get names of all "up" network interfaces (linux only) 
Originally published: 2005-08-11 13:17:36 
Last updated: 2005-08-11 13:17:36 
Author: paul cannon 
 
Uses the SIOCGIFCONF ioctl to obtain a list of interfaces and extracts those names, returning them in a list of strings.