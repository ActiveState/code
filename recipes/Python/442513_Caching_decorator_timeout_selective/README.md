###Caching decorator with timeout, selective invalidation

Originally published: 2005-11-02 02:47:48
Last updated: 2005-11-05 05:47:03
Author: Greg Steffensen

A caching decorator that garbage collects in a separate thread (for performance), allows each cached function to (optionally) set a custom maximum age for entries, and allows individual cache entries to be selectively invalidated.