## Populate SQL tables from CSV data files

Originally published: 2011-02-02 21:21:49
Last updated: 2011-02-02 21:21:49
Author: James Mills

Just a quick recipe I developed a few years ago that I thought\nmight be useful to others. Basically it takes as input a\ndata file with comma separated values (CSV) and translates\nthis into a series of SQL "INSERT" statements allowing you\nto then feed this into MySQL, SQLite, or any other database.\n\nExample Usage:\n\n$ cat cars.csv \nYear,Make,Model,Length\n1997,Ford,E350,2.34\n2000,Mercury,Cougar,2.38\n\n$ sqlite3 cars.db "CREATE TABLE cars (Year, Make, Model, Length)"\n\n$ ./csv2sql.py cars.csv | sqlite3 cars.db \n\n$ sqlite3 cars.db "SELECT * FROM cars"\n1997|Ford|E350|2.34\n2000|Mercury|Cougar|2.38\n\nEnjoy! Feedback welcome!\n\ncheers\nJames Mills / prologic