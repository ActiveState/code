## Async subprocess check_output replacement for Twisted 
Originally published: 2012-01-20 09:48:26 
Last updated: 2012-01-20 09:48:27 
Author: Alan Franzoni 
 
As any twisted user knows, the original python subprocess module can yield to interferences with twisted's own reactor - at least unless installSignalHandlers is false, which can lead to other consequences. \n\nThis recipe simulates a stripped down version of subprocess.check_output() which returns a deferred and is twisted friendly.