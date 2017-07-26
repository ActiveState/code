## JSON instead of pickle for memcachedOriginally published: 2012-01-10 22:31:36 
Last updated: 2012-01-10 22:31:36 
Author: pavel  
 
Standard memcache client uses pickle as a serialization format. It can be handy to use json, especially when another component (e.g. backend) does'n know pickle, but json yes.