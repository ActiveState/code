## Copy gmail.com contacts onto your mobile phone via gnokii  
Originally published: 2006-01-08 12:28:48  
Last updated: 2007-05-23 05:51:27  
Author: Scott Tsai  
  
This script uses the csv module to convert gmail.com contacts data to the "raw" gnokii phonbook format,
which is another CSV variant, while preserving cell/home/work/fax numbers, street address, URL and notes data entries.

gnokii (www.gnokii.org) is an open source program for communicating with mobile phones
that runs under Windows and Linux/Unix.
Note that gmail.com supports exporting contacts in both Outlook and Gmail CSV formats.
This script needs the Gmail format.

Run this script with a command like:
cat gmail.csv | gmail-csv-to-gnokii | gnokii --writephonebook --overwrite