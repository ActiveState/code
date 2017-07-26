## Converting MySQL database to an Amazon Simple DB database  
Originally published: 2008-10-31 11:55:16  
Last updated: 2008-10-31 11:55:16  
Author: Chris McAvoy  
  
This script will take all the tables from a given MySQL database and upload them to Amazon SimpleDB as Domains.  The 'name' of each uploaded record is the value of the first primary key found in the table.\n\nThis was written to scratch a particular itch, I've tested it against a 500mb database of my own, but didn't try overly hard to make it an all purpose general tool.