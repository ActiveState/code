## Server side JavaScript dependency resolution  
Originally published: 2006-11-15 09:53:45  
Last updated: 2006-11-15 09:53:45  
Author: Michael Palmer  
  
Purpose: Easing maintenance of JavaScript files and their inclusions in web pages by server-side dependency resolution. If at the top of a.js you include the comment

// requireScript b.js

and at the top of b.js you say

// requireScript c.js

then JSResolver's method .asTags('a.js') will give you e.g.

&lt;script language="javascript" src="c.js"&gt;&lt;/script&gt;
&lt;script language="javascript" src="b.js"&gt;&lt;/script&gt;
&lt;script language="javascript" src="a.js"&gt;&lt;/script&gt;

which you can then stick straight into your web page.

Circular dependencies between JS files are forbidden and raise an exception.