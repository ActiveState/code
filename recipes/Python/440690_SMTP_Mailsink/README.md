## SMTP Mailsink  
Originally published: 2005-10-11 11:00:32  
Last updated: 2005-10-11 11:00:32  
Author: Adam Feuer  
  
This little class starts up an SMTP server which acts as an email sink, collecting all received emails destined for any address. All emails are routed to a Portable Unix Mailbox file. This is very handy for testing applications that send email. It runs in its own thread, so you can easily use it from a test fixture to collect your emails and verify them for correctness.