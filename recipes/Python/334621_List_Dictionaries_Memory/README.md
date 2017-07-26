## A List of Dictionaries, for the Memory Scrooge.Originally published: 2004-11-06 19:56:20 
Last updated: 2004-11-09 00:39:18 
Author: S W 
 
I often return result sets from a database call using a list of dictionary objects. When transmitting the pickled list object over the wire, the size of the pickle greatly effects the speed of the transmission.\n\nI wrote this small class to emulate a list of dictionary objects without the memory and pickle storage overhead which occurs when storing every item in the list as a dictionary.