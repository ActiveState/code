## Automation of unix shell or DOS shell programs  
Originally published: 2007-11-12 20:22:43  
Last updated: 2007-11-14 02:31:49  
Author: Peter Dilley  
  
Every view months HP provides new SNMP MIB files for their new products (software and hardware). Using the provided HP shell commands mcompile and mxmib, you compile and register each .mib/.cfg file with their management software on a file by file basis. This script automates the process.

Shows:
o Automation of shell commands
o Using script/shell arguments
o Error checking
o OS independent file, path, directory handling
o Sequential programming

Prerequisites:
This script assumes you have HP Systems Insight Manager installed to provide the mcompile and mxmib programs if you wish to run it directly on your system.