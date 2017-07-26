###Authenticate with twisted.web.xmlrpc

Originally published: 2006-02-07 15:44:52
Last updated: 2006-09-05 18:09:47
Author: Duncan McGreggor

These classes subclass several of the culprits in twisted.web.xmlrpc that are responsible for not being able to make autenticated XML-RPC calls.\n\nNote that this recipe also makes use of the URI classes that were posted in a previous recipe here:\n  http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/473864\n\nI will submit a patch to twisted along these lines, but there will be no references to the custom Uri module or code.\n\nUpdate: XML-RPC Authentication is now supported in Twisted (version 2.4 included a patch based on this recipe). If you are using a recent version of Twisted or can update to a recent version, this recipe is no longer needed.