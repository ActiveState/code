## Generate java structure definitions for DB2 tables.  
Originally published: 2003-06-18 01:33:12  
Last updated: 2003-06-18 01:33:12  
Author: Patrick Finnegan  
  
This tcl script, called from a windows bat file generates java structure definitions for DB2 tables using the db2 db2dclgn and describe utilities.

Output is sent to two files.

*.txt

452   CHARACTER            1  ACCESS_STATUS                               13
485   DECIMAL           8, 0  CUSTOMER                                     8

*.java

java.lang.String	access_status;
java.math.BigDecimal 	customer;