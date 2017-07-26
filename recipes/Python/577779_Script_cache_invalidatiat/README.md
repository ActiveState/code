## Script for cache invalidation at Amazon CloudFront  
Originally published: 2011-07-05 14:34:41  
Last updated: 2011-07-05 14:40:58  
Author: Andrey Nikishaev  
  
This script scans directories that was uploaded to CloudFront and build files index. When you modify some files, script automatically see what files was modified since the last update, and clear cache on CloudFront only for them.


Usage: script.py data_dir [index_file] [dir_prefix] 

data_dir       - path to directory with uploaded data

index_file     - path to files index

dir_prefix     - needed if you data_dir path is different from url at CloudFront.For example: Your data_dir is '/data' but url at CloudFront is http://url.com/social/data/ so dir_prefix will be '/social/data/'