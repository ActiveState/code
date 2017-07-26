## Script for GAE Blobstore migration from Master Slave to High Replication Datastore 
Originally published: 2011-11-03 17:21:03 
Last updated: 2011-11-04 14:56:56 
Author: Tomáš Rampas 
 
This code helped me with blobstore content migration of my GAE app from M/S storage to HRD. Prerequisite for this is copying data located in Masterslave datastore to HRD first so they exist on both Datastores.\nBe aware pls, that this migration script has impact on outgoing and incoming bandwidth of your apps so it affects your GAE resources utilization.