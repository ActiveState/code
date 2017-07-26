## Singleton? We don't need no stinkin' singleton: the Borg design patternOriginally published: 2001-08-17 07:42:57 
Last updated: 2001-08-27 08:05:21 
Author: Alex Martelli 
 
The Singleton design pattern (DP) has a catchy name, but the wrong focus -- on identity rather than on state.  The Borg design pattern has all instances share state instead, and Python makes it, literally, a snap.