###rdd (mostly broken but shows how to do a few things in ruby)

Originally published: 2012-02-06 04:44:06
Last updated: 2014-07-12 16:58:06
Author: Mike 'Fuzzy' Partin

Meant to be a slightly more "advanced" dd utility. Supporting FTP/File/STDIN as input streams, and File/STDOUT/PIPE as output targets, and sporting a progress display (very rudimentary atm), add lets you combine network, and file or pipe processing in a single command. But kind of ended up a mess, see the [Python version](https://code.activestate.com/recipes/578907-python-awesome-dd/?in=user-4179778) which is pretty clean.