###Paypal IPN

Originally published: 2005-11-18 08:16:10
Last updated: 2006-09-19 19:02:54
Author: Anthony Barker

This is a cgi script that allows you to log an ipn request from paypal. Basically if you configure your paypal account with an ipn url it will send a post to a script url. You need to respond with a post and then will receive a VERIFIED response.\n\nI've included a subroutine to log the data to a database, but you could simply use a text file if that is all you need.