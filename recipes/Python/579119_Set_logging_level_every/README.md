## Set the logging level to every logger

Originally published: 2015-10-28 23:16:25
Last updated: 2015-10-28 23:16:26
Author: Tim McNamara

Python's logging allocates a name to every logger. That makes it hard to do something like, setting everything to `logging.ERROR`. Here's one way you might go about that: