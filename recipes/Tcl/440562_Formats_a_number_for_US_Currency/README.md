## Formats a number for US Currency  
Originally published: 2005-09-15 14:52:09  
Last updated: 2005-09-15 14:52:09  
Author: Richard Zimmerman  
  
I was in need of a routine to format numbers for a revenue report. I found Andreas Kupries (http://aspn.activestate.com/ASPN/Cookbook/Tcl/Recipe/146220) routine to reformat a number to insert the commas but it didn't address the decimal position alignment. tcl [format] string could format the decimal positions but not insert the commas. So I used Andreas base code and extended it.