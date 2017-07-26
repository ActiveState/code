## Foreign Exchange Rate Alert, CSV version ($CAD<->$USD)  
Originally published: 2003-12-17 09:41:55  
Last updated: 2011-12-09 07:32:23  
Author: Victor Yang  
  
* The following code snippet can be used as daily crontab or windows scheduled task to watch the foreign exchange rate from BankOfCanada web site. 
* The file format is not fancy XML but a simple CSV for noon rate for last 5 days.  

* urllib2.urlopen is used as it can auto detect the proxy if it is used. 
* The default url connnect timeout is 60 seconds here.

