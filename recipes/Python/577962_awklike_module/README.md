## awk-like module  
Originally published: 2011-11-25 17:14:56  
Last updated: 2011-11-25 17:14:57  
Author: david   
  
This python module is similar to awk (pattern scanning and processing language in unix/linux).\nIt scans the input file for lines, split each line to fields.\n        *._nr   # AWK NR\n        *._nf   # AWK NF\n        *._0r  # AWK $0\n        *._1   # AWK strip($1)\n        *._1r  # AWK $1 , raw string\n        *._1i  # AWK int($1)\n        *._1f  # AWK float($1)