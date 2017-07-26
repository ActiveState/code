## Read OpenOffice Spreadsheet as list of lists (without UNO) 
Originally published: 2005-07-06 01:02:48 
Last updated: 2005-11-28 11:34:46 
Author: Romano Giannetti 
 
This is a quick-and-dirty snippet that read a OpenOffice 1.1 spreadsheet (.sxc files) as a list of lists, every list representing a oocalc row. The row contents are unicode object with the "string" content of the cell. This snippet used as a program will convert .sxc files into comma-separated-values (csv) on the command line. Style is not perfect and could be greatly enhanced, but it works for me as is...