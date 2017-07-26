## Performance boost with metaclasses

Originally published: 2013-02-17 10:58:13
Last updated: 2013-02-17 10:58:13
Author: Martin Schoepf

Consider a highly dynamic system where a lot of objects are created and destroyed. If the objects are complex and have a lot of default values the following recipe may improve the performance. The more default values you have the more you will gain from it. 