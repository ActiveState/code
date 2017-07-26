###Remove control character ^M from opened html files

Originally published: 2004-07-12 18:51:02
Last updated: 2004-07-12 18:51:02
Author: Liang Guo

I used a URLOpener to get the HTML file from some web-sites for some parsing. However, the returned data file had ^M everywhere, and it was pretty annoying. Before parsing this file, I want to strip it of all occurences of this control character ^M. Of course, I can use dos2unix or similar tools to do that offline, but I wanna do it the pythonic way.\n\nFirst, I need to find out the ascii value for '^M'.\n\n>>> import curses.ascii\n>>> ascii.ascii('^V^M')\n'\\r'\n\nThen, I can just do a search and replace '\\r' in any string.\n\n>>> string.replace( str, '\\r', '' )\n\nIn my code, I just have this line in the overriden method handle_data of my html parser class.