###Safe HTML string and unicode

Originally published: 2012-01-09 18:29:20
Last updated: 2012-01-10 08:14:14
Author: Garel Alex

As you display message on a web page, you have to sanitize input data coming from users to avoid [XSS](https://en.wikipedia.org/wiki/Cross-site_scripting). Here is a small recipe where we can use a special class for our string to be sure we get safe all the way long.