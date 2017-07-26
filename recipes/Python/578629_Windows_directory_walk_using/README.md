## Windows directory walk using ctypesOriginally published: 2013-08-09 00:15:08 
Last updated: 2013-08-09 00:17:00 
Author: Shao-chuan Wang 
 
Windows shell/explorer has a limit size of full path, but both NTFS and ReFS can support full path longer than the limit; this is making os.walk on Windows bad if files are in deeply nested folders, and therefore this recipe.