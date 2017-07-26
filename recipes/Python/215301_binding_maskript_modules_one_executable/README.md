## binding main skript and modules to one executable with python-2.3 under UNIX  
Originally published: 2003-08-11 05:44:03  
Last updated: 2003-08-11 05:44:03  
Author: Joerg Raedler  
  
Some python applications contain a main skript and some additional modules. By using zipimport from python-2.3 and some help of the shell one may bind all needed files (except the python interpreter and its standard modules) into one executable. This eliminates the need for an expensive installation.