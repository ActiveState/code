## Simple conversion of excel files into CSV and YAMLOriginally published: 2008-02-14 00:39:22 
Last updated: 2008-02-14 00:39:22 
Author: Philip Kromer 
 
Takes an excel file, dumps out a series of CSV files (one for each sheet, named for the file and sheet) and a YAML file (an array of sheets, each sheet a dict containing the table_name and the table_data, a 2-d array of cell values).\n\nInspired by Bryan Niederberger's "Easy Cross Platform Excel Parsing With Xlrd", http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/483742  As opposed to his code, this script makes no attempt to understand the structure of the sheet (look for header cells, etc) -- it simply reads, converts, dumps.