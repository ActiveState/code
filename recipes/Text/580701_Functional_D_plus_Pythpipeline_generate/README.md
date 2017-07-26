## Functional D plus Python pipeline to generate PDF  
Originally published: 2016-09-22 15:32:16  
Last updated: 2016-09-22 15:32:17  
Author: Vasudev Ram  
  
This recipe is a command pipeline. The first component of the pipeline is a D language program that makes use of simple functional programming and template / generic programming features of D, to transform some input into the desired output. Both input and output are text. The D program writes the output to standard output, which is then read by a Python program that reads that as input via standard input, and converts it to PDF.
