## Shelf alternative using hashed keys as filenames and pickled values  
Originally published: 2008-01-24 10:24:31  
Last updated: 2008-01-24 10:24:31  
Author: Brian Bush  
  
Shelving dictionaries are quick and easy, until they grow too large and access is slowed to a crawl. This recipe is a directory cache with the filename an md5 of the key and the value is the file contents (as a pickled dump).