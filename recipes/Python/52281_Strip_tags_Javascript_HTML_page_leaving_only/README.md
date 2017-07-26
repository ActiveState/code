## Strip tags and Javascript from HTML page, leaving only safe tagsOriginally published: 2001-03-19 12:58:08 
Last updated: 2001-03-19 12:58:08 
Author: Itamar Shtull-Trauring 
 
Sometimes we are getting HTML input from the user.  We want to only allow valid, undangerous tags, we want all tags to be balanced (i.e. an unclosed <b> will leave all text on your page bold), and we want to strip out all Javascript.\n\nThis recipe demonstrates how to do this using the sgmllib parser to parse HTML.