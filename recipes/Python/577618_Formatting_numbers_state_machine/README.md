## Formatting numbers with a state machine (implementation of a regex pattern)  
Originally published: 2011-03-22 03:39:36  
Last updated: 2011-03-22 03:40:45  
Author: James Mills  
  
I was once asked to explain how the following regular expression works which formats any integer with commas for every thousand (or group of 3 digits):\n    \n    (\\d)(?=(\\d{3})+$)\n    \n\nExample:\n    \n    >>> import re\n    >>> re.sub("(\\d)(?=(\\d{3})+$)", "\\\\1,", "1234")\n    '1,234'\n    \n\nSo here is an implementation of the above regular expression (as best as I could over a lunch break) that will hopefully highlight\nhow a regular expression engine and finite automa work.\n\nComments and feedback welcome!\n\n--JamesMills / prologic