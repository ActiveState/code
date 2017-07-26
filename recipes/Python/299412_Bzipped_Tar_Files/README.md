###Bzipped Tar Files

Originally published: 2004-08-12 06:49:44
Last updated: 2004-08-17 20:27:16
Author: Ed Gordon

I was working on a backup utility to compress files and folders into a .tar.bz2 file and found the documentation and internet info to be a bit lacking. So here is an example for those that tackle this in the future.\n\nI initially thought, "Hey, there is a 'tarfile' module and a bz2 module, so I am good to go." Not that easy. The bz2 module does not accept tarfile objects for compression. I hunted around the documentation a and found that bzipping is part of an 'open' class method for a tarfile. But once you make a tarfile.TarFile object, it is too late. Instead, you have to create the tarfile object with 'tarfile.TarFile.open(destination, 'w:bz2'. So here is an example.