## MySQL-based forum functions  
Originally published: 2007-06-08 08:43:19  
Last updated: 2007-06-08 08:43:19  
Author: Calder Coalson  
  
This program provides the basic functions required to write a forum in MySQL and Python.  The way the class is structured allows it to be imported and used in any application, whether it's web based, command line, Tcl/Tk or wxPython.  It simply provides the helper functions to perform actions required to get, use and set different data in the database.

However, I have not included the code to create the database yet.  Here's the structure:
TABLE: users
    INTEGER: id
    STRING: name
    STRING: signature
    STRING: password
TABLE: messages
    INTEGER: id
    LONGSTRING: content
    DATE: created
    TIME: createdtime
    DATE: edited
    TIME: editedtime
    INTEGER: authorid
TABLE: threads
    INTEGER: id
    STRING: title
    STRING: messages
    DATETIME: edited

Create that database, set up a user account, and change the arguments in ForumBase.__init__ to the user you want the program to log on as.