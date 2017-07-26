## A Phone Book GUI Built in wxPython Connected To Database Using Data Grid View  
Originally published: 2013-09-29 14:59:08  
Last updated: 2013-09-29 19:25:23  
Author: toufic zaarour  
  
this GUI as simple as it is explains some basic but important graphical database interfacing; "Add", "Edit","Delete","Search" and few others along with a data grid view. in order to work create an sqlite3 database as follows:

data table : Phone,
column 1 : ID,
column 2 : name,
column 3 : surname,
column 4 : telephone.

save the sqlite3 file as file.db in a folder called Data and place it in the same directory as your python script.

if you want to create the sqlite3 database graphically use my previous post : http://code.activestate.com/recipes/578665-a-wxpython-gui-to-create-sqlite3-databases/

Also there is more: I did not use auto-number for 'id' because I also wanted to include in the code a renumbering script.

 I am pleased to receive all the suggestions and improvements on this site or to my e-mail directly if this is convenient to you.

note: if you don't like the database table name, and columns name create your own but make sure to change them in the code as well! in the end life is great! remember that!