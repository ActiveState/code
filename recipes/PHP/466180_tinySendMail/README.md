## tinySendMail

Originally published: 2006-01-08 14:14:49
Last updated: 2006-01-08 14:14:49
Author: Dave Silvia

Frequently the mail functions of php are inaccessible due to no access to a sendmail or equivalent binary and/or non-configuration in php.ini on a given server.  This code (function) allows sending mail in most all cases, the only requirement is the ability to open a socket in php!;)