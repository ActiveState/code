## passwd-file-compatible ($1$) MD5 cryptOriginally published: 2004-10-26 13:58:15 
Last updated: 2004-10-26 13:58:15 
Author: Mark Johnston 
 
A port of Poul-Henning Kamp's MD5 password hash routine, as initially found in FreeBSD 2.  It is also used in Cisco routers, Apache htpasswd files, and other places that you find "$1$" at the beginning of password hashes.