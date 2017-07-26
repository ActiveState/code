## Extracting Windows file versions  
Originally published: 2001-09-03 21:59:14  
Last updated: 2001-09-10 16:29:25  
Author: Joshua Biagio  
  
This is my attempt at extracting the file version information\nfrom .dll, .exe, .ocx files etc. on Windows 2000\n(should work with others, but I haven't tested it),\nwithout resorting to using extensions (i.e. dll functions).\n\nIt is "Pure Python"... but unfortunately is not\ndocumented very well. Please let me know if it helps you!\n\nPut the code in a file in your PYTHONPATH (such as 'verchecker.py')\nand say 'from verchecker import *'. You may then get version\ninfo by executing: calcversioninfo('path/filename')\n\n-Joshua W. Biagio -- jw_SPAM_biagio@juno.com (remove _spam_)\n