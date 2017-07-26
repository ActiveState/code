## Watching a directory tree under Linux

Originally published: 2003-08-25 01:36:49
Last updated: 2003-08-25 01:36:49
Author: Keith Dart

Inspired by another snippet here that watches a directory... Here is a directory watcher that only works on Linux, as it uses the asyncronous directory notify feature. It will generate a SIGIO on directory change. You should define a signal handler that calls this back (actaully, calls the instance).