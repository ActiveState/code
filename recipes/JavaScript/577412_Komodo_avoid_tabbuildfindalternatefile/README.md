## Komodo: avoid tab-buildup with a find-alternate-file macro 
Originally published: 2010-09-28 18:16:41 
Last updated: 2010-09-28 18:16:42 
Author: Eric Promislow 
 
In Emacs I used to use find-alternate-file all the time to replace the current buffer with a different one, usually one in the same directory. Komodo doesn't provide an off-the-shelf way to do this, and if you can't be bothered to close buffers when you no longer need them, you'll soon suffer from the dreaded tab buildup problem, up there with the heartbreak of browser tab overload. But it's easy to write a macro to avoid this. 