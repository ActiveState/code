###Copy gmail.com contacts onto your mobile phone via gnokii

Originally published: 2006-01-08 12:28:48
Last updated: 2007-05-23 05:51:27
Author: Scott Tsai

This script uses the csv module to convert gmail.com contacts data to the "raw" gnokii phonbook format,\nwhich is another CSV variant, while preserving cell/home/work/fax numbers, street address, URL and notes data entries.\n\ngnokii (www.gnokii.org) is an open source program for communicating with mobile phones\nthat runs under Windows and Linux/Unix.\nNote that gmail.com supports exporting contacts in both Outlook and Gmail CSV formats.\nThis script needs the Gmail format.\n\nRun this script with a command like:\ncat gmail.csv | gmail-csv-to-gnokii | gnokii --writephonebook --overwrite