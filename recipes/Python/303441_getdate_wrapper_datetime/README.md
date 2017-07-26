## get_date wrapper to datetime module 
Originally published: 2004-09-04 07:35:42 
Last updated: 2004-09-04 07:35:42 
Author: John Nielsen 
 
The datetime module only accepts inputs of time it understands. For example,\nthe months given to it have to be in range of values 1-12. This wrapper works around that issue and enables you to move forward or backward more arbitrary units of time. It does that by changing the year, month, and day to fit the requirements of datetime.