## getting process information on windows

Originally published: 2004-09-03 11:10:53
Last updated: 2004-09-03 11:10:53
Author: John Nielsen

To get process information for both NT and W2K (but not the 9x family) you can use the Performance Data Helper library(PDH). The is a simple example that shows you how to get a process list and their ids. It provides a convenient interface to performance information stored fundamentally in the registry. The basic process of using the PDH encompasses the following:\n\n   1. Get a list of all the objects you want\n   2. Get a list of the object's instances and data available for each instance: called 'items' or 'counters'\n   3. Get a group of performance data for each counter\n\nIn the case here we want the process object, the object's instances are it's list of processes, and the counter we want for the processes is 'ID Process'.