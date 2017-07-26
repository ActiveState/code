###Dictionary / Class / List Indexes into Database Query Results

Originally published: 2008-02-18 21:49:31
Last updated: 2008-02-18 21:49:31
Author: Kevin Ryan

Similar to some other recipes on this site, this script allows you to access results from queries by attribute (eg, row.field_name), by key (eg, row['field_name']) or by Index (eg, row[0] or row[:2], etc.).  It is different from other recipes in that it is both light-weight and offers a variety of access methods with very little overhead.  Improvements could be made in fetching the query results (ie, right now I just fetchall()), but I'll leave that up to you.