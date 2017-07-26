## A File-Like Object to True File Object Adapter  
Originally published: 2003-05-28 12:14:05  
Last updated: 2003-05-28 12:14:05  
Author: Michael Kent  
  
Sometimes you have a file-like object (such as what urllib.urlopen() returns), but you need to pass it to a function/method that insists on receiving a true file object (what the file or open built-in functions give you).  What you need is a adapter to turn your file-like object into a true file object.