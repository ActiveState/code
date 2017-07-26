## pytunnel: tunneling w/threads (ssl thru proxy in this case) 
Originally published: 2003-07-30 15:15:44 
Last updated: 2005-12-30 14:16:43 
Author: John Nielsen 
 
This code shows an implementation of tunneling. Though this code uses ssl as an example. It would not be hard to modify it to work for other situations as well.\n\nThe reason I use ssl as an example is because the standard python libraries do not support tunneling ssl through a proxy. Import pytunnel and give it a function w/the code you want to tunnel and your off.\n\nFor the latest code try:\nhttp://ftp.gnu.org/pub/savannah/cvs/pytunnel-cvs-latest.tar.gz