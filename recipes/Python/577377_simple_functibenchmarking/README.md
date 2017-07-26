## A simple function benchmarking module

Originally published: 2010-08-27 09:26:47
Last updated: 2010-08-27 09:26:48
Author: Timothee Cezard

This module enable its user to monitor the amount of time spend in between two commands start and stop.\nThe module is fairly imprecise if the monitored task is quick as the start and stop commands are fairly slow (2e-07 - 5e-07 second)