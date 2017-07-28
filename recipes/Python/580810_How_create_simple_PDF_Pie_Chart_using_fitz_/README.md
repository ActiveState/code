## How to create a simple PDF Pie Chart using fitz / PyMuPDF  
Originally published: 2017-07-10 16:07:51  
Last updated: 2017-07-10 16:07:51  
Author: Jorj X. McKie  
  
PyMuPDF now supports drawing pie charts on a PDF page.

Important parameters for the function are center of the circle, one of the two arc's end points and the angle of the circular sector. The function will draw the pie piece (in a variety of options) and return the arc's calculated other end point for any subsequent processing.

This example creates a chart of the parliament seat distribution for political parties in the current German Bundestag.