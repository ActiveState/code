## Complex Boolean Regular Expression Class  
Originally published: 2003-12-11 00:56:07  
Last updated: 2003-12-19 13:12:13  
Author: Anand   
  
Very often we need to look for the occurence of words in a string or group of words. We rely on regular expressions for such operations. A very common requirement is to look for the occurence of certain words in a paragraph or string. We can group the occurence by boolean operators AND, OR and NOT, allowing to search for certain words using boolean logic.\n\nThis class is created to do exactly that. It wraps up a\ncomplex boolean word expression, creating an internal\nregular expression, and provides methods allowing you to\nperform matches and searches on it.