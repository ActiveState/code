## gzip pipe for asynchronous use

Originally published: 2008-03-21 15:23:04
Last updated: 2008-03-24 21:47:17
Author: Raphaël Jolivet

I've written a small class to handle a gzip pipe that won't read the whole source file at once, but will deliver small chunks of data on demand.\n\n