## Purge Mysql binary logs  
Originally published: 2010-01-12 14:43:44 
Last updated: 2010-01-12 15:14:10 
Author: Umang Gopani 
 
Being a MySQL DBA , one faces a common issue in replication environment -> Disk space issue on master, since the number of binary logs have increased.\nNow, one of the solution to this would be using expire_logs_days parameter in your mysql config file.\nBut what if, the slave is lagging by few hours or if the slave is broken since few days and the binary logs are removed due to the parameter set. Whenever the salve comes up, it will go bonkers, knowing that the binary log where it last stopped no more exists.\n\nI faced this issue a couple of time until I decided to automate it using a script. Herewith I am attaching a python script which can run regularly in cron.\n