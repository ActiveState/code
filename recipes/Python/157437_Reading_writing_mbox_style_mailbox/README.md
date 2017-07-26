## Reading and writing mbox style mailbox files.Originally published: 2002-10-18 12:06:30 
Last updated: 2002-10-18 12:06:30 
Author: Noah Spurrier 
 
This script demonstrates reading and writing an mbox style mailbox. This script is an mbox filter. It scans through an entire mbox and writes the messages to a new file. Each message is passed through a filter function which may modify the document or ignore it.