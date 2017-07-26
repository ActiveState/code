## Batch conversion of text files to PDF with fileinput and xtopdf  
Originally published: 2016-11-07 20:28:01  
Last updated: 2016-11-07 20:28:01  
Author: Vasudev Ram  
  

This recipe shows how to do a batch conversion of the content of multiple text files into a single PDF file, with a) an automatic page break after the content of each text file (in the PDF output), b) page numbering, and c) a header and footer on each page.

It uses the fileinput module (part of the Python standard library), and xtopdf, a Python library for conversion of other formats to PDF.

xtopdf is available here: https://bitbucket.org/vasudevram/xtopdf

and a guide to installing and using xtopdf is here:

http://jugad2.blogspot.in/2012/07/guide-to-installing-and-using-xtopdf.html

Here is a sample run of the program:

python BTTP123.pdf text1.txt text2.txt text3.txt

This will read the content from the three text files specified and write it into the PDF file specified, neatly formatted.


