###Memoize Decorator with Timeout

Originally published: 2004-10-31 18:41:36
Last updated: 2004-11-02 07:16:11
Author: S W

This simple decorator is different to other memoize decorators in that it will only cache results for a period of time. It also provides a simple method of cleaning the cache of old entries via the .collect method. This will help prevent excessive or needless memory consumption.