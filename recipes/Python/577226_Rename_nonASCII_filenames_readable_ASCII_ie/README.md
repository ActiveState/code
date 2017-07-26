## Rename non-ASCII filenames to readable ASCII, i.e. replace accented characters, etc  
Originally published: 2010-05-12 12:54:46  
Last updated: 2011-11-03 17:50:55  
Author: ccpizza   
  
The script converts any accented characters in filenames to their ASCII equivalents. e.g.:\n\nExample:\n\n    â > a\n    ä > a\n    à > a\n    á > a\n    é > e\n    í > i\n    ó > o\n    ú > u\n    ñ > n\n    ü > u\n    ...\n\nBefore-and-after example:\n\n    01_Antonín_Dvořák_Allegro.mp3   >>>  01_Antonin_Dvorak_Allegro.mp3\n\n\nUsage:\n\n    Running the script without arguments will rename all files in the current folder. \n    !!!WARNING!!! ***No*** backups are created.