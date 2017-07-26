## ftpfind.py: a command-line tool that combines the functionality 'find' and 'ftp'.  
Originally published: 2005-07-07 10:25:51  
Last updated: 2005-07-07 10:25:51  
Author: Guy Argo  
  
On several occasions I wanted to peruse an FTP site for a specific rpm within
a certain age range and with a particular pattern to its filename and none of
the tools available gave me that functionality. This recipe gives a find-like
tool to the world of FTP. Great for cron jobs that download new RPMs that fit
some tricky condition (e.g. less than 1 meg, less than a week old, ends in
x86_64.tar.gz etc).