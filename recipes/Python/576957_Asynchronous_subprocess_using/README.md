## Asynchronous subprocess using asyncore 
Originally published: 2009-11-13 11:04:37 
Last updated: 2013-01-21 19:51:00 
Author: Glenn Eychaner 
 
A coroutine-based wrapper for subprocess.Popen that uses asyncore to communicate with child processes asynchronously.  This allows subprocesses to be called from within socket servers or clients without needing a complicated event loop to check both. Uses recipe 576965 to provide the asynchronous coroutine framework, recipe 576967 to provide asynchronous pipes, and recipe 577600 to provide multiple alarms.