###Querying an online dictionary

Originally published: 2002-06-11 15:29:11
Last updated: 2002-06-11 15:29:11
Author: andreas kupries

Origin: http://wiki.tcl.tk/3211\nAuthor: Reinhard Max.\n\nThis little script sends it's command line arguments as a query to the online dictionary at http://dict.leo.org and writes the parsed result to stdout. It uses Tcl's http package and the htmlparse and ncgi packages from Tcllib.\n\nThe scraper part (everything inside the ::dict.leo.org namespace) could also be included from other frontends. It's [query] proc takes a list of words to search for, and returns a list of english/german pairs that matched the query.