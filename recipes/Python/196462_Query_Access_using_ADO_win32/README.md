## Query Access using ADO in win32 platform  
Originally published: 2003-04-24 22:38:00  
Last updated: 2003-04-24 22:38:00  
Author: Souman Deb  
  
Dependencies 1) Windows Machine, 2) Python2.2 with win32 extensions installed 3) Apache Webserver for win32\nThis code queries the Northwind Database's "Order Details" Table..Make sure the path of the DB is correct and the query u are using is also accurate cause this does not give any error outputs but writes it in Apache's error.log file...\ncopy this file in the cgi-bin directory and call it from the web browser as http://localhost/cgi-bin/ADO.py (file name). The only problem is the currency field, I cannot obtain the currency field properly it is obtained as a tuple !! hope u can help me ! :)