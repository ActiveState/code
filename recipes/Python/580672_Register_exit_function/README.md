## Register exit function

Originally published: 2016-05-31 00:33:11
Last updated: 2016-05-31 00:42:47
Author: Giampaolo Rodolà

This is a function / decorator which registers a function which will be executed on "normal" interpreter exit or in case one of the `signals` is received by this process (differently from atexit.register()). Also, it makes sure to execute any other function which was previously registered via signal.signal(). If any, it will be  executed after our own `fun`. The full blogpost explaining why you should use this instead of atexit module is here: http://grodola.blogspot.com/2016/02/how-to-always-execute-exit-functions-in-py.html