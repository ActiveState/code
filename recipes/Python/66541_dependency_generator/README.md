## dependency generator for makefiles  
Originally published: 2001-08-20 09:41:55  
Last updated: 2001-08-20 18:10:33  
Author: Will Ware  
  
This script scans .c files for "#include" statements and creates a list of\ndependencies, suitable for inclusion in a makefile. Name this script "mkdep"\nand then type "mkdep *.c"; dependencies will come out standard output.