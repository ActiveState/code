## JACL script to purge messages on IMAP server

Originally published: 2005-11-10 23:13:32
Last updated: 2005-11-10 23:13:32
Author: D. J. Hagberg

This script was written before I found out about the Cyrus "ipurge" command.  It connects to a Cyrus IMAP server as the administrator, finds all Trash folders and deletes all messages older than 1 day based on the Received date.  Requires JavaMail's mail.jar and activation.jar in the classpath.