###SQL Column width from delimited text

Originally published: 2006-09-22 23:12:52
Last updated: 2006-09-22 23:12:52
Author: Matt Keranen

When loading text files into database tables (MSSQL in this example), the source columns often do not match the table definition. This script was written to find the maximum length of each column in a delimited text file, then modify the a table create DDL file to make each character column wide enough, so truncation errors do not occur.