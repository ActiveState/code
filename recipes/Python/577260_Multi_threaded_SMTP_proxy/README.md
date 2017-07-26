## Multi threaded SMTP proxy 
Originally published: 2010-06-12 22:25:42 
Last updated: 2010-06-12 22:27:00 
Author: Lobsang  
 
This smtp proxy can be used to process any part of the message (header and body). It is also possible to process all the body part just before it is send to the MTA.\n\nThe aim of this proxy is to allow a modification of the message on the fly. It had been tested with the postfix  [before queue content filter](http://www.postfix.org/SMTPD_PROXY_README.html)