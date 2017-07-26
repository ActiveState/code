## Locating files throughout a directory treeOriginally published: 2006-12-12 08:42:09 
Last updated: 2009-12-02 07:30:27 
Author: Simon Brunning 
 
os.walk is a very nice replacement for os.path.walk, which I never did feel comfortable with. There's one very common pattern of usage, though, which still benefits from a simple helper-function; locating all files matching a given file-name pattern within a directory tree.