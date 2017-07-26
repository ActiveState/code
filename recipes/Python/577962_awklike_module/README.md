## awk-like module  
Originally published: 2011-11-25 17:14:56  
Last updated: 2011-11-25 17:14:57  
Author: david   
  
This python module is similar to awk (pattern scanning and processing language in unix/linux).
It scans the input file for lines, split each line to fields.
        *._nr   # AWK NR
        *._nf   # AWK NF
        *._0r  # AWK $0
        *._1   # AWK strip($1)
        *._1r  # AWK $1 , raw string
        *._1i  # AWK int($1)
        *._1f  # AWK float($1)