###Python reader for SPSS .por files

Originally published: 2009-06-15 15:37:39
Last updated: 2009-06-15 15:37:39
Author: wouter 

SPSS can output ASCII .por files that include variable definitions (labels, value labels) and data. These files are useful to be able to read but strange enough I couldn't find any documentation anywhere.\n\nI've reverse engineered the format so that it works for the (fairly complex) files I need to open, so maybe it is of some use for other people interfacing SPSS with python. \n\nThis code is placed in the public domain as far as allowed by law, parts (if any) that cannot be relased in the public domain are irrevocably licensed to all readers under the Creative Commons license without restrictions ... but if you improve it it would be great if you could share it. The code uses a base N decoder plucked from the web somewhere (can't find it) that was also public domain.\n\n-- wouter (wouter@vanatteveldt.com)