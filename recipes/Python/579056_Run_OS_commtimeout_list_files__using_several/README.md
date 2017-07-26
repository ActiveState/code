## Run OS command with timeout on a list of files  using several threads

Originally published: 2015-05-19 13:02:20
Last updated: 2015-05-19 19:31:59
Author: Antoni Gual

This hack runs a command sequentially on a list of files using two simultaneous threads. If one of the commands takes more than a set time, it's killed and the program goes for the next file. EDITED to add some exception handling.