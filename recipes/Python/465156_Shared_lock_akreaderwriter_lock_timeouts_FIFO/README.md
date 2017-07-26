## Shared lock (aka reader-writer lock) with timeouts and FIFO ordering  
Originally published: 2005-12-20 21:56:24  
Last updated: 2005-12-20 21:56:24  
Author: Dmitry Dvoinikov  
  
This shared lock implementation supports timeouts so that an attempt to acquire a lock occasionally times out. It also preserves FIFO ordering for threads waiting for exclusive lock and has other valuable features.