## Server side JavaScript dependency resolution  
Originally published: 2006-11-15 09:53:45  
Last updated: 2006-11-15 09:53:45  
Author: Michael Palmer  
  
Purpose: Easing maintenance of JavaScript files and their inclusions in web pages by server-side dependency resolution. If at the top of a.js you include the comment\n\n// requireScript b.js\n\nand at the top of b.js you say\n\n// requireScript c.js\n\nthen JSResolver's method .asTags('a.js') will give you e.g.\n\n&lt;script language="javascript" src="c.js"&gt;&lt;/script&gt;\n&lt;script language="javascript" src="b.js"&gt;&lt;/script&gt;\n&lt;script language="javascript" src="a.js"&gt;&lt;/script&gt;\n\nwhich you can then stick straight into your web page.\n\nCircular dependencies between JS files are forbidden and raise an exception.