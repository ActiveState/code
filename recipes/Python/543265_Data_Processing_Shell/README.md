## Data Processing Shell

Originally published: 2008-01-24 16:26:43
Last updated: 2008-01-24 16:26:43
Author: Brian Davis

I've found that I frequently need to open a file, do some processing on it and then load it into excel. This script provides a nice interface for opening the file using a wxPython dialog box, some code to load the result .csv file into excel using win32com and a function to contain the processing code. I should probably turn this into a module sometime...