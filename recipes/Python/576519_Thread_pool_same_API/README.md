## Thread pool with same API as (multi)processing.Pool

Originally published: 2008-10-01 15:40:55
Last updated: 2016-01-30 00:40:20
Author: david decotigny

There are probably <write your guess here>s of recipes presenting how to implement a pool of threads. Now that multiprocessing is becoming mainstream, this recipe takes multiprocessing.Pool as a model and re-implements it entirely with threads. Even the comments should look familiar... This recipe also adds 2 new methods: imap_async() and imap_unordered_async().