## Create SQL tables from CSV files  
Originally published: 2006-09-22 23:24:39  
Last updated: 2010-02-24 13:47:36  
Author: Matt Keranen  
  
Script generates CREATE TABLE statements based on the width of data present in comma delimited (csv) test files. Setting the correct datatypes (other than VARCHAR), is still a manual adventure.

## TODOs:
 - Eliminate '#N/A', '@NA' from data
 - Remove commas from numeric data
 - Check for duplicate column names
 - Create BCP format file or INSERT statements?