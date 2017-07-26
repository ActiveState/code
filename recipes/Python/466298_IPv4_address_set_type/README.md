## IPv4 address set type 
Originally published: 2006-01-15 10:46:18 
Last updated: 2006-01-23 15:52:38 
Author: Heiko Wundram 
 
Building on another recipe of mine (http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/466286) this is a set type for storing IPv4 address(-ranges) efficiently. It parses several different formats for specifying IPv4 address ranges described in the docstrings, and allows you to output the contained addresses as ip/mask or ip-ip pairs, and also allows you to iterate over all ip addresses.