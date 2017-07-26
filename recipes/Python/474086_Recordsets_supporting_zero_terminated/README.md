## Recordsets supporting zero terminated stringsOriginally published: 2006-02-25 15:10:17 
Last updated: 2006-02-25 15:10:17 
Author: Andre Pfeuffer 
 
There has been a receipe already, but not supporting zero terminated 'C' strings. Zerotermination is marked with 'z', number before 'z', say 2z is not supported. You can use 2 'z' positions, however. Set tu=True outputs to [] instead of record.