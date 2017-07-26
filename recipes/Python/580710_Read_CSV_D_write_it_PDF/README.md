## Read CSV with D and write it to PDF with Python  
Originally published: 2016-10-26 17:49:00  
Last updated: 2016-10-26 17:49:00  
Author: Vasudev Ram  
  
\nThis recipe shows how to read data from a CSV file with a D program and write that data to a PDF file with a Python program - all in a single command-line invocation (after writing the individual programs, of course).\n\nIt requires the xtopdf toolkit, which you can get from:\n\nhttps://bitbucket.org/vasudevram/xtopdf\n\nInstructions for installing xtopdf:\n\nhttp://jugad2.blogspot.in/2012/07/guide-to-installing-and-using-xtopdf.html\n\nxtopdf in turn requires the open source version of the ReportLab toolkit, which you can get from:\n\nhttp://www.reportlab.com/ftp (http://www.reportlab.com/ftp/reportlab-1.21.1.tar.gz)\n\nIt also requires the DMD compiler to compile the D program - this was the version used:\n\nDMD32 D Compiler v2.071.2\n\n