## Pretty and Stated HTMLParsers  
Originally published: 2013-12-13 13:52:39  
Last updated: 2013-12-14 00:28:36  
Author: Ádám Szieberth  
  
Extensions of html.parser.HTMLParser().

PrettyHTMLParser() does not splits data into chuncks by HTML entities.
StatedHTMLParser() can have many state-dependent handlers which helps parsing HTML pages alot.