## Precise console progress meter with ETA calculation  
Originally published: 2010-01-11 09:37:48  
Last updated: 2010-04-18 21:11:40  
Author: Denis Barmenkov  
  
After several attempts to use third-party modules I wrote my own console progress meter.\n\nBonus list:\n\n1. calculation of ETA based on last update points. More accuracy when comparing with calculation ETA based on process start time (process can survive after Hibernate, but ETA has lost his accuracy)\n2. ability to write progress meter to sys.stderr\n3. update_left() method for multithreaded programs :)