## Formating strings (print a table)  
Originally published: 2013-06-18 07:44:09  
Last updated: 2013-06-18 07:52:03  
Author: greg zakharov  
  
As you know there are no escape characters such as "\\t" in the windows command language but it does not mean that we can not format text. Command prompt has its own tricks. At firstly, you need declare enabledelayedexpansion after setlocal command in your batch file to get access for some interesting things; secondly, use <code><nul set /p "str=[string]"</code> construction which is equal print function in C language. OK, next batch file print multiplication table.