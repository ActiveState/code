The steps for this recipe are as follows:

1. Download the selpg utility from its repository on Bitbucket:

https://bitbucket.org/vasudevram/selpg/src

including all these files: makefile, mk, selpg.c and showsyserr.c

2. Build the selpg utility by running the shell script called mk. It calls the make command which uses the C compiler on your Linux system to compile and link the source code.

This will result in a binary called selpg.

3. Install ReportLab v1.21, which is a dependency for xtopdf, from http://www.reportlab.com/ftp , by downloading either the .zip or the .tar.gz file from there, extracting its contents into some new folder, and following the instructions in the README or INSTALL file.

4. Install xtopdf in some new folder, following the instructions given here:

http://jugad2.blogspot.in/2012/07/guide-to-installing-and-using-xtopdf.html

(The instructions are for Windows, but anyone with basic Linux experience can easily adapt them for Linux, since the task only requires uncompressing the xtopdf zip or tar.gz file and setting an environment variable or two.)

The above steps are a one time task.

5. After that, you can run this pipeline whenever you wish, with appropriate values for the name of the input text file and the output PDF file, to select a range of pages from any text file and print them to PDF:

$ ./selpg -s2 -e4 input_file.txt | python StdinToPDF.py output_file.pdf

where you have to replace the 2 in the -s2 with the start page number, and the 4 in the -e4 with the end page number, of the range of pages that you wish to print to the PDF file.

More details are available at this blog post:

http://jugad2.blogspot.in/2014/10/print-selected-text-pages-to-pdf-with.html
