###building a crontab to start jobs in hourly batches (administrators one-stop-shopping)

Originally published: 2007-05-28 00:41:47
Last updated: 2007-05-28 00:41:47
Author: Peter Arwanitis

Task: Administrative job to run in my case 2300 jobs in a scheduled manner\nRestriction: Don't start two jobs at same schedule on same server\n\nProblems to solve that for:\n* align list of projects into batch of jobs with distinct servers\n* templated job creation\n* create a crontab\n * to start all this jobs from a starting schedule every hour\n * respect some restrictions that on some days and some hours no jobs should be started\n\nThanks to builtin map() and standard-library time, datetime and timedelta to make that an ease at the end!