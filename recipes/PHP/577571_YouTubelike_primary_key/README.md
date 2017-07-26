## YouTube-like primary key generation  
Originally published: 2011-02-11 00:53:32  
Last updated: 2011-02-24 21:43:55  
Author: Slava Yanson  
  
If you have more then 1 primary database servers - you have probably experienced the pain of primary key overlapping... Here is a super simple solution that will generate a hash of random letters and numbers.\n\nIncluded is a sample ActiveRecord class (MyTable.php).