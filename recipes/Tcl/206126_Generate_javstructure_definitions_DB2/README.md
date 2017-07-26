## Generate java structure definitions for DB2 tables.  
Originally published: 2003-06-18 01:33:12  
Last updated: 2003-06-18 01:33:12  
Author: Patrick Finnegan  
  
This tcl script, called from a windows bat file generates java structure definitions for DB2 tables using the db2 db2dclgn and describe utilities.\n\nOutput is sent to two files.\n\n*.txt\n\n452   CHARACTER            1  ACCESS_STATUS                               13\n485   DECIMAL           8, 0  CUSTOMER                                     8\n\n*.java\n\njava.lang.String\taccess_status;\njava.math.BigDecimal \tcustomer;