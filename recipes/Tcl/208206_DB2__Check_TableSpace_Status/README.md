## DB2 - Check TableSpace Status  
Originally published: 2003-07-01 00:06:47  
Last updated: 2003-07-01 00:06:47  
Author: Patrick Finnegan  
  
DB2 tablespaces can become unavailable for various reasons and when they do go off-line the problem may not be immediately visible.  For example tablespaces in "backup pending mode" can be readable but not updateable.

For example:


------------------------------ Command Entered ------------------------------
update sch1.table1set ind = 'N' where provider = 'ABC'

-----------------------------------------------------------------------------
DB21034E  The command was processed as an SQL statement because it was not a
valid Command Line Processor command.  During SQL processing it returned:
SQL0290N  Table space access is not allowed.  SQLSTATE=55039

This looks like a permissions problem but it's actually an issue with the physical tablespace.  We can enumerate the tablespace details with the "db2 list tablespaces".  In this case the hex code for the "state" command indicates backup pending.

Table

Tablespace ID                        = 91
Name                                 = SW380
Type                                 = System managed space
Contents                             = Any data
State                                = 0x0020
Detailed explanation:
    Backup pending

This procedure returns a list of tablespaces where state is abnormal.