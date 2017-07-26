## using the operator  module  w/map (plus a bit on  itertools and  generator exp)Originally published: 2004-09-21 15:58:52 
Last updated: 2004-09-22 12:39:17 
Author: John Nielsen 
 
These are just some simple examples of how you can leverage the operator module to   help gain performance with something like map (it works great with sort too). There are times where techniques like this may be necessary. Generally, you'd want to avoid doing this simply because it makes python ugly and harder to debug.