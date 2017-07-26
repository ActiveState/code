## Filtering CSV data by fields (cut for csv)  
Originally published: 2011-02-02 21:39:45  
Last updated: 2011-02-02 21:39:45  
Author: James Mills  
  
Ever wanted to take a CSV file as input, cut it up
and only extract the fields that you want ?

Here's how!

$ cat cars.csv 
Year,Make,Model,Length
1997,Ford,E350,2.34
2000,Mercury,Cougar,2.38

$ csvcut.py -f 0 -f -1 - < cars.csv 
Year,Length
1997,2.34
2000,2.38

--JamesMills (prologic)