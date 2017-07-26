## ObjectMerger 
Originally published: 2004-03-04 20:53:04 
Last updated: 2004-03-05 15:44:56 
Author: Alejandro David Weil 
 
The ObjectMerger class dynamically merges two given objects, making one a subclass of the other. The input elements could either be class instances or simple types, making this class particularly useful to derive native classes (for instance, cStringIO).\nThe resulting ObjectMerger instance acts as a proxy to the new type, allowing callers to work with it in the same way they would work with any other statically derived type.