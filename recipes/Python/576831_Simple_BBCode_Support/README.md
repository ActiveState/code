###Simple BBCode Support

Originally published: 2009-07-04 18:39:06
Last updated: 2009-07-04 20:03:55
Author: Stephen Chappell

After trying to write a BBCode support library, I decided that less in more. Though incomplete in its support of BBCode, it handles most cases with a minimal amount of code. Simply type "BBCode." followed by the operator. Call this with the text to be wrapped along with any arguments that operator may take. The virtual methods are case-sensitive, but the rendered names are returned in upper-case. If you are trying to write some forum-related software and want a lite BBCode implimentation, this recipe may serve your purposes well. The only aspect of this project that might be fixed at the user's discretion is support for numbered and bulleted lists (to be added to the _BBCode class as methods).