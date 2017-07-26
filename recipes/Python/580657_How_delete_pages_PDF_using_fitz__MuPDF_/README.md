## How to delete pages in a PDF using fitz / MuPDF / PyMuPDF  
Originally published: 2016-05-01 09:26:43  
Last updated: 2016-05-01 09:26:44  
Author: Jorj X. McKie  
  
A new method **select()** in PyMuPDF 1.9.0 allows selecting pages of a PDF document to create a new one. Any Python list of integers (0 <= n < page count) can be taken.

The resulting PDF contains all links, annotations and bookmarks (provided they still point to valid targets).