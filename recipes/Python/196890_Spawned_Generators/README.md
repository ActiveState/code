## Spawned Generators  
Originally published: 2003-04-27 16:25:56  
Last updated: 2003-04-27 16:25:56  
Author: Garth Kidd  
  
The SpawnedGenerator class, initialised with a generator, will run that generator in a separate thread and either yield successive values obtained from it (when called) or let you iterate itself to get the same results. It's mainly useful for tasks which make blocking OS calls, e.g. traversing directory structures. The queue size may be specified to limit how far ahead of the main task the spawned generator can get.