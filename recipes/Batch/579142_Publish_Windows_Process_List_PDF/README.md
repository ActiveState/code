## Publish a Windows Process List to PDF with xtopdf

Originally published: 2015-12-27 20:45:31
Last updated: 2015-12-27 20:45:32
Author: Vasudev Ram

This recipe shows how you can generate a Windows process list or task list (basically, a list of running processes, with some information about each of them), to a PDF file, using the Windows TASKLIST command along with the xtopdf toolkit. The list is sorted in ascending order of memory usage of the processes, before writing it to PDF.\n\nIt differs somewhat from other xtopdf recipes, in that no additional code needs to be written, over and above what is already in the xtopdf package. We just have to use the needed commands there, in a series of commands or a pipeline.\n\nHowever, one can still write additional code, by modifying the program used (StdinToPDF.py), if needed, to customize the PDF output.\n\n