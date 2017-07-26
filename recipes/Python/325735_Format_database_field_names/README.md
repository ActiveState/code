###Format database field names in Excel

Originally published: 2004-10-29 12:56:29
Last updated: 2004-10-29 19:57:50
Author: Matt Keranen

Often I get data to import in MS Excel files, and the column headers are not very useful for column names. They contain spaces, punctuation, and special characters that make a simple import difficult.\n\nThis script opens the file in Excel, and applies some simple formatting rules to the first row and addresses duplicate names. Then when the file is imported (SQL Server DTS in my case), the column names are somewhat usable.