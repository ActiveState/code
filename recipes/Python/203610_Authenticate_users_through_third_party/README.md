## Authenticate users through a third party POP-server 
Originally published: 2003-06-03 15:51:09 
Last updated: 2003-06-03 15:51:09 
Author: Magnus Lyckå 
 
Here's an example of how an existing POP-mail account can be used to provide authentication to a python application.\n\nThe user doesn't have to remember yet another password, and the administrator doesn't have to handle users who forgot... Instead, we associate all our users to some external POP-mail account. When they want to log in to our system, we ask them for the password to their email account.\n\nIf we can log in to the pop server using their password, and just get a status from their mailbox (we don't peek of course) we decide that the user has authenticated himself.