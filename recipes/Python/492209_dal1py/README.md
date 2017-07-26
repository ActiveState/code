## dal_1.py

Originally published: 2006-04-26 09:45:27
Last updated: 2006-04-26 09:45:27
Author: Stephen Chappell

The class presented bellow (Disk Abstraction\nLayer 1) is designed to provide a very easy\ninterface to work with secondary memory\nwhere IO errors may occur and data is\nworked with in blocks. DAL1 allows access\nto a hard drive (via its driver) so that\nit can be accessed in a file-like way.\nIO errors are also taken care of at this\nlevel (which can cause problems at extremely\nhigh probabilities of failure.