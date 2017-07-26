## Count up transfer for 3 mobile broadband on a mac  
Originally published: 2009-01-04 03:13:33  
Last updated: 2009-01-04 03:13:33  
Author: Anand Patil  
  
The 3 (a UK mobile carrier) broadband dongle is handy, but its mac support is really awful. In particular, the interface software doesn't provide any straightforward way to see your total data transfer to date. This can lead to nasty surprises if you're using a pay-as-you-go plan.\n\nThis executable scans /var/log/ppp.log and totals up your data transfers over your dongle. It can optionally take a date as a command-line argument, in which case it only totals up usage after the given date.