###Voxel Based Ray Tracing

Originally published: 2013-08-29 06:11:40
Last updated: 2013-08-29 06:11:41
Author: FB36 

The standard ray tracing algorithm seems unnatural to me because everytime a ray reflects/refracts all (primitive) objects in the scene must be tested for intersection; no matter where they located!\n\n\nIn this method there is no such thing. It just moves each ray voxel by voxel until it hits an opaque/reflective(/refractive) voxel.\n\n\nI made many simplifications so the image is crude.