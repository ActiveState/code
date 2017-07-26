## Nagios plugin for monitoring database servers  
Originally published: 2011-03-07 04:04:00  
Last updated: 2011-08-23 22:12:20  
Author: Matt Keranen  
  
An example implementation of a Nagios script in Python for monitoring database servers via ODBC queries. The example tests contained are for checking the status of MS SQL Server replication and log shipping, but any status check that can be performed by a query can be implemented. This method is not considered a replacement for SNMP monitoring, but to implement custom logic checks.\n\nNew tests are implemented by adding an @nagios_test decorator, and called by the -t parameter with the function name. Usage text list available tests.