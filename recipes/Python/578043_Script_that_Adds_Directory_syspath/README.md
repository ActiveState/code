## A Script that Adds a Directory to sys.path Permanently 
Originally published: 2012-02-16 23:15:10 
Last updated: 2012-02-16 23:15:11 
Author: Eric Snow 
 
This script takes advantage of PEP 370, "Per user site-packages directory".  It manages .pth files, which are are non-volatile (unlike manually adding to sys.path).  See http://docs.python.org/library/site.html.