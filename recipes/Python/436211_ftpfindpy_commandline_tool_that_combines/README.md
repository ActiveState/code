###ftpfind.py: a command-line tool that combines the functionality 'find' and 'ftp'.

Originally published: 2005-07-07 10:25:51
Last updated: 2005-07-07 10:25:51
Author: Guy Argo

On several occasions I wanted to peruse an FTP site for a specific rpm within\na certain age range and with a particular pattern to its filename and none of\nthe tools available gave me that functionality. This recipe gives a find-like\ntool to the world of FTP. Great for cron jobs that download new RPMs that fit\nsome tricky condition (e.g. less than 1 meg, less than a week old, ends in\nx86_64.tar.gz etc).