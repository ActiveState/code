## extend textwrap.TextWrapper to handle multiple paragraphs 
Originally published: 2004-12-11 02:04:02 
Last updated: 2004-12-11 02:04:02 
Author: Brett Cannon 
 
textwrap is a very handy module.  The problem with it, though, is that it expects to be used with individual paragraphs.  But what if you want to wrap an entire document?  It will still wrap the lines, but it will improperly consider it all a single paragraph.\n\nThis recipe alleviates that issue by overriding textwrap.TextWrapper.wrap with an implementation that handles spiltting a document into paragraphs and processing each individually.  This allows things such as initial_indent to work as expected.