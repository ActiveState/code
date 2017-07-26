###For Characters in a String, Replace with Character

Originally published: 2012-03-23 20:16:12
Last updated: 2012-03-23 20:44:23
Author: Andrew Yurisich

Useful if you need to replace many different characters with all of the same character. Can accept an unlimited number of request to replace.\n\nDoes not work with words, only characters. You can, however, replace single characters with words. I may go back and re-implement it using tuples for the keys, but this would make searching the text for any matches pretty expensive, I'd imagine. At that point, it's mostly a job for a regex, and those tools already exist.