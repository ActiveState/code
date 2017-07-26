## Top 20 linux distributions  
Originally published: 2009-03-15 08:32:36  
Last updated: 2009-03-15 08:32:36  
Author: Agnius Vasiliauskas  
  
Script for calculating top 20 most popular linux distributions.
This is done by getting list of possible linux distributions from http://lwn.net/Distributions/.
And after that - automated queries are send to yahoo search engine to get a pages count which every distribution returns. From these numbers linux distribution rating is built as percentage from total top 20 queries hits.

IMPORTANT: because there are about 300 queries which are send to yahoo,- load of yahoo server is pretty high, so for load balancing each query is send with 2 seconds delay. Despite to this there is a good chance to get temporary ban from yahoo search service, because of high load from one IP address. SO, USE AT YOUR OWN RISK !!!