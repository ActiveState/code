## Strip attachments from an email messageOriginally published: 2004-08-26 06:08:02 
Last updated: 2004-08-26 06:08:02 
Author: anthony baxter 
 
This recipe shows a simple approach to using the Python email package to strip out attachments and file types from an email message that might be considered dangerous. This is particularly relevant in Python 2.4, as the email Parser is now much more robust in handling mal-formed messages (which are typical for virus and worm emails)