## SystemMutex

Originally published: 2015-01-09 10:14:15
Last updated: 2015-01-09 10:14:15
Author: Fabio Zadrozny

This module provides a way to create a mutex which is valid for the system (i.e.: it can be seen by multiple processes).\n\nNote that the mutex is kept until release_mutex() is called or when it's garbage-collected.