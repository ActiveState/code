## Fuzzy matching dictionary 
Originally published: 2006-03-18 11:23:25 
Last updated: 2006-03-18 11:23:25 
Author: Mark Mc Mahon 
 
This is more an ease of use subclass of dict - rather then one that uses a lot of dict features.\n\nIf your requested item is in the dictionary (with a key that hashes the same) then it acts as a more or less normal dictionary.\n\nIf on the other hand you are looking for a string that is similar to a key in the dictionary, then the class iterates over all the keys and finds the one that is the closest match.