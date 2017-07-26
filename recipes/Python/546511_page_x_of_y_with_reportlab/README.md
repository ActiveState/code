## "page x of y" with reportlab  
Originally published: 2008-02-12 09:38:32  
Last updated: 2008-02-13 14:27:33  
Author: hermes tresmegistos  
  
This approach at the common "page x of y" problem avoids a double pass (creating the pdf document twice).\nThis is achieved by a customized canvas class which saves the codes into a list instead of creating postscript on pagebreak (showPage). When the document should be saved, we recall each page and draw the pageinfo.\nThe trick is that you can modify the canvas of each page until it is saved (meaning you already know the total pagecount).