## Populate SQL tables from CSV data files  
Originally published: 2011-02-02 21:21:49  
Last updated: 2011-02-02 21:21:49  
Author: James Mills  
  
Just a quick recipe I developed a few years ago that I thought
might be useful to others. Basically it takes as input a
data file with comma separated values (CSV) and translates
this into a series of SQL "INSERT" statements allowing you
to then feed this into MySQL, SQLite, or any other database.

Example Usage:

$ cat cars.csv 
Year,Make,Model,Length
1997,Ford,E350,2.34
2000,Mercury,Cougar,2.38

$ sqlite3 cars.db "CREATE TABLE cars (Year, Make, Model, Length)"

$ ./csv2sql.py cars.csv | sqlite3 cars.db 

$ sqlite3 cars.db "SELECT * FROM cars"
1997|Ford|E350|2.34
2000|Mercury|Cougar|2.38

Enjoy! Feedback welcome!

cheers
James Mills / prologic