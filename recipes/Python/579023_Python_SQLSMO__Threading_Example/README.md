## Python SQLSMO - Threading Example  
Originally published: 2015-02-10 01:56:09  
Last updated: 2015-02-10 02:01:42  
Author: Jorge Besada  
  
This is an example of the use of the SQLSMO module. Using a csv file DBLIST_ACTIONS.csv  with list of databases where you can launch multiple different database operations in parallel

Some lines of the configuration file DBLIST_ACTIONS.csv used shown below:
SERVERNAME,DBNAME1,SOURCESERVER,DATAFOLDER,LOGFOLDER,DBNAME2,ACTIONS,ENABLED
(local)\sql2014,AdventureWorks2012,C:\SQL2014\BACKUPS,C:\SQL2014\DATA,C:\SQL2014\LOG,AdventureWorks_COPY1,RESTOREDBS1.CFG,Y
(local)\sql2014,AdventureWorks2012,C:\SQL2014\BACKUPS,C:\SQL2014\DATA,C:\SQL2014\LOG,AdventureWorks_COPY2,RESTOREDBS1.CFG,Y
(local)\sql2014,AdventureWorks2012,C:\SQL2014\BACKUPS,C:\SQL2014\DATA,C:\SQL2014\LOG,AdventureWorks_COPY3,RESTOREDBS1.CFG,Y
(local)\sql2014,AdventureWorks2012,C:\SQL2014\BACKUPS,C:\SQL2014\DATA,C:\SQL2014\LOG,AdventureWorks_COPY4,RESTOREDBS1.CFG,

Where:
SERVERNAME: server where the database to act upon resides

DBNAME1: source database

DBNAME2: destination database (may be different from source when we restore a copy with a different name)

SOURCESERVER: this is the network (or local) folder where backups are placed

DATAFOLDER: folder for data files

LOGFOLDER: folder for log files

ACTIONS: this is the name of the configuration file (.CFG) with the list of actions

ENABLED: a Y value here will mean we want to process the line



For each line (database) you specify a configuration file (in this case RESTOREDBS1.CFG), see sample below:
(one line for each, no blank lines)

RESTORE DATABASE

SET DBOWNER: sa

SYNC LOGINS

SET SIMPLE MODE

SHRINK LOG



The program will process each line in the source CSV file and for each one it will perform the set of operations described in the configuration file. This system is being used in my workplace with different configuration files for different databases (there are configuration files for restores, specific restores with more actions, backups, etc, not included here for brevity).

Every time you do a database task you just add a line in the DBLIST_ACTIONS.CSV and create (if needed) a configuration file). If you are going to actually use it include a "Y" in the ENABLED column
Note: every line action in the configuration file must have been implemented in the function ActionParsing as one the entries in the big if statement.

Special features:
You can specify at the start of the program if you want to really execute or not. You may want to do first a trial run setting NOEXECUTE_OPTION = 1 (instead of the default of 0). In this case the program will run and create the SQL script of the operations, not executing them. 
Note: it has been implemented in the restores so far, will add it to the other options later.

Threading: by default it will run as many threads as lines in the DBLIST_ACTIONS.CSV file. But you can change this option by setting a value to THREAD_POOL different than 0. 
