## Reimplementation of rmtree supporting Windows reparse pointsOriginally published: 2014-03-08 20:34:59 
Last updated: 2014-03-08 21:17:41 
Author: Charles Grunwald 
 
Ctypes-based implementation of shutil.rmtree that correctly handles Windows reparse point folders. (symbolic links, junctions, etc)