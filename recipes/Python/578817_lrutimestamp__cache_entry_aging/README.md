###lru_timestamp - cache entry aging for functools.lru_cache

Originally published: 2014-02-02 11:07:43
Last updated: 2014-02-02 21:28:25
Author: Peter Santoro

Return a timestamp string for @lru_cache decorated functions.\n\nThe returned timestamp is used as the value of an extra parameter\nto @lru_cache decorated functions, allowing for more control over\nhow often cache entries are refreshed. The lru_timestamp function\nshould be called with the same refresh_interval value for a given\n@lru_cache decorated function.  The returned timestamp is for the\nbenefit of the @lru_cache decorator and is normally not used by\nthe decorated function.\n\nPositional arguments:\nrefresh_interval -- in minutes (default 60), values less than 1\n                    are coerced to 1, values more than 1440 are\n                    coerced to 1440