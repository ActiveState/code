## building a crontab to start jobs in hourly batches (administrators one-stop-shopping)  
Originally published: 2007-05-28 00:41:47  
Last updated: 2007-05-28 00:41:47  
Author: Peter Arwanitis  
  
Task: Administrative job to run in my case 2300 jobs in a scheduled manner
Restriction: Don't start two jobs at same schedule on same server

Problems to solve that for:
* align list of projects into batch of jobs with distinct servers
* templated job creation
* create a crontab
 * to start all this jobs from a starting schedule every hour
 * respect some restrictions that on some days and some hours no jobs should be started

Thanks to builtin map() and standard-library time, datetime and timedelta to make that an ease at the end!