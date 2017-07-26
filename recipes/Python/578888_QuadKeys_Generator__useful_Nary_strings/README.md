###QuadKeys Generator - useful for N'ary strings generation

Originally published: 2014-06-12 10:29:34
Last updated: 2014-06-12 10:29:35
Author: Narayana Chikkam

As per the standard articles available on the internet, world map could be divided into four section top left, top right, bottom left and bottom right. if we associate numbers to identify them, for eg:\n0 -> top left\n1 -> top right\n2 -> bottom left\n3 -> bottom right\nit would be easier to dig into a tile or a section of the map using this system. A good documentation on the same is available on the 'Bing Map Tile System'. It would be a good idea to have some snippet of code that generates these sequence of numbers in this system so that world map could be traversed in a serial fashion. The class has 3 generator methods that produce the same sequence. Width corresponds to the zoom level.