## Improvements of the urllib.URLopen.retrieve() method 
Originally published: 2010-01-16 04:50:07 
Last updated: 2010-01-16 04:50:07 
Author: Kévin Gomez 
 
I improved the urllib.URLopen.retrieve() method so that it can restart a download if it failed. And like wget does (with wget -c), it restarts where it stopped.\nThe number of maximum tries can be changed.