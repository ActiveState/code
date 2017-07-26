## Convert JSON to PDF with Python and xtopdf  
Originally published: 2014-12-10 18:02:13  
Last updated: 2014-12-10 18:02:14  
Author: Vasudev Ram  
  
This recipe show the basic steps needed to convert JSON input to PDF output, using Python and xtopdf, a PDF creation toolkit. xtopdf is itself written in Pytho, and uses the ReportLab toolkit internally.

We set up some needed values, such as the output PDF file name, the font name and size, the header and footer, and the input lines for the body of the PDF output; all these values are passed in JSON format (in a single dictionary) to a function that uses those values to generate a PDF file with the desired content.
 
The code is intentionally kept simple so as to require the least amount of code needed to demonstrate the techniques involved. But it can be generalized or extended to more complex situations.
