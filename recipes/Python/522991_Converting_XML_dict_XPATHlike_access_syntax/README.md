## Converting XML to dict (for a XPATH-like access syntax) and back to XML  
Originally published: 2007-06-25 06:23:51  
Last updated: 2007-06-28 03:16:28  
Author: Rodrigo Strauss  
  
I really like config files done in Python language itself, using a dictionary declaration. It's cool for programmers, but not so cool for system administrators not used to Python (it's so easy to forget a comma...).\nTo keep using dictionaries internally providing something more admin friendly, I've done some functions to convert a XML file to Python dictionary (and the reverse as well):