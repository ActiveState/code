## lru_timestamp - cache entry aging for functools.lru_cache  
Originally published: 2014-02-02 11:07:43  
Last updated: 2014-02-02 21:28:25  
Author: Peter Santoro  
  
Return a timestamp string for @lru_cache decorated functions.

The returned timestamp is used as the value of an extra parameter
to @lru_cache decorated functions, allowing for more control over
how often cache entries are refreshed. The lru_timestamp function
should be called with the same refresh_interval value for a given
@lru_cache decorated function.  The returned timestamp is for the
benefit of the @lru_cache decorator and is normally not used by
the decorated function.

Positional arguments:
refresh_interval -- in minutes (default 60), values less than 1
                    are coerced to 1, values more than 1440 are
                    coerced to 1440