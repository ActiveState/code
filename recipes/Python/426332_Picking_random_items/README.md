## Picking random items from an iterator 
Originally published: 2005-06-22 01:57:25 
Last updated: 2005-06-22 01:57:25 
Author: Simon Brunning 
 
Each item has an equal chance of being picked.  The iterator is processed only once, and only the selected items are stored, making this function memory efficient.\n\nThis is based on idea from Richard Papworth's recipe that picks a random from a file - see http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/59865 - but is more general.