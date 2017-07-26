## How to use twisted pb FilePagerOriginally published: 2009-04-30 05:18:11 
Last updated: 2009-04-30 05:20:09 
Author: alex lavoro.propio 
 
Banana limits string objects to 640k so sending a large file requires to break it into many small chunks. Twisted provide a helper class to do this: twisted.spread.pb.FilePager. I modified on recipe 457670: "How to use twisted pb pager" to demonstrate the usage of FilePager. getFile1() is similar to getIt() in recipe 457670. getFile2() uses the utility function in twisted.spread.pb.util.