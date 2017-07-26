## Revisiting "Revenge of the auto-wrap": Another toggle-macro 
Originally published: 2010-10-04 17:17:18 
Last updated: 2010-10-04 23:51:41 
Author: Eric Promislow 
 
Komodo doesn't automatically wrap lines when they reach a certain length, which is a good trait to have in a code editor. However, for those times where you're editing non-code, it can be helpful to have newlines inserted automatically. Troy Topnik addressed this problem a couple of years ago, in his post http://www.activestate.com/blog/2008/11/revenge-auto-wrap-type-type-type-ding . As Komodo 6 heads out the door, I've been writing blog posts, and found this feature useful. But his solution used two macros. I put my coding hat back on, and reimplemented it as a "toggle macro".