## Filtering CSV data by fields (cut for csv)

Originally published: 2011-02-02 21:39:45
Last updated: 2011-02-02 21:39:45
Author: James Mills

Ever wanted to take a CSV file as input, cut it up\nand only extract the fields that you want ?\n\nHere's how!\n\n$ cat cars.csv \nYear,Make,Model,Length\n1997,Ford,E350,2.34\n2000,Mercury,Cougar,2.38\n\n$ csvcut.py -f 0 -f -1 - < cars.csv \nYear,Length\n1997,2.34\n2000,2.38\n\n--JamesMills (prologic)