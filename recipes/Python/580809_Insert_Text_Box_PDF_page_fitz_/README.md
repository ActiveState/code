## Insert a Text Box in a PDF page (fitz / PyMuPDF)  
Originally published: 2017-06-29 22:54:24  
Last updated: 2017-06-29 22:54:25  
Author: Jorj X. McKie  
  
This method inserts text into a predefined rectangular area of a (new or existing) PDF page.
Words are distributed across the available space, put on new lines when required etc. Line breaks and tab characters are respected / resolved.
Text can be aligned in the box (left, center, right) and fonts can be freely chosen.
The method returns a float indicating how vertical space is left over after filling the area.