## Extracting Windows file versions  
Originally published: 2001-09-03 21:59:14  
Last updated: 2001-09-10 16:29:25  
Author: Joshua Biagio  
  
This is my attempt at extracting the file version information
from .dll, .exe, .ocx files etc. on Windows 2000
(should work with others, but I haven't tested it),
without resorting to using extensions (i.e. dll functions).

It is "Pure Python"... but unfortunately is not
documented very well. Please let me know if it helps you!

Put the code in a file in your PYTHONPATH (such as 'verchecker.py')
and say 'from verchecker import *'. You may then get version
info by executing: calcversioninfo('path/filename')

-Joshua W. Biagio -- jw_SPAM_biagio@juno.com (remove _spam_)
