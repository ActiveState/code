## Use generators for fetching large db record sets  
Originally published: 2002-07-02 07:02:51  
Last updated: 2010-02-10 10:47:53  
Author: Christopher Prinos  
  
When using the python DB API, it's tempting to always use a cursor's fetchall() method so that you can easily iterate through a result set. For very large result sets though, this could be expensive in terms of memory (and time to wait for the entire result set to come back). You can use fetchmany() instead, but then have to manage looping through the intemediate result sets. Here's a generator that simplifies that for you.