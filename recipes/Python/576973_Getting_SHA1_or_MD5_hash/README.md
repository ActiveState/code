## Getting the SHA-1 (or MD5) hash of a directory 
Originally published: 2009-11-28 23:25:38 
Last updated: 2009-12-06 19:02:40 
Author: Stephen Akiki 
 
http://akiscode.com/articles/sha-1directoryhash.shtml\n----------------------------------------------------------------------------------------------\nBy definition a cryptographic hash is, "a deterministic procedure that takes an arbitrary block of data and returns a fixed-size bit string, the (cryptographic) hash value, such that an accidental or intentional change to the data will change the hash value". \n\nUsually these hashes are used on files to "fingerprint" them, but in order to do the same to a directory you have to do something like this: 