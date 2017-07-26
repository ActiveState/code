## Rename non-ASCII filenames to readable ASCII, i.e. replace accented characters, etc  
Originally published: 2010-05-12 12:54:46  
Last updated: 2011-11-03 17:50:55  
Author: ccpizza   
  
The script converts any accented characters in filenames to their ASCII equivalents. e.g.:

Example:

    â > a
    ä > a
    à > a
    á > a
    é > e
    í > i
    ó > o
    ú > u
    ñ > n
    ü > u
    ...

Before-and-after example:

    01_Antonín_Dvořák_Allegro.mp3   >>>  01_Antonin_Dvorak_Allegro.mp3


Usage:

    Running the script without arguments will rename all files in the current folder. 
    !!!WARNING!!! ***No*** backups are created.