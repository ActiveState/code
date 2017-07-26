## Fuzzy Google truth

Originally published: 2002-06-11 15:40:48
Last updated: 2002-06-11 15:40:48
Author: andreas kupries

Origin: http://wiki.tcl.tk/3490\nAuthor: Richard Suchenwirth\n\nGiven some piece of data where it is doubtful whether they are correct or not, one way to find out is just to ask a search engine like Google, but disregard the results except for the number of found web pages. Chances are that the correct data have a higher hit rate than the faulty one.\n\n\nExample output in the text widget (asking about a city in Italy, where post code and province were unsure):\n 'bellaria rn': 3580 hits\n 'bellaria fo': 609 hits\n 'bellaria 47814': 1130 hits\n 'bellaria 47014': 30 hits\n\nThese results seem to indicate that 47814 Bellaria RN (Rimini) is the correct address ;-) On single words one might use this for spelling verification:\n 'suchenwirth': 280 hits\n 'suchenworth': 0 hits\n\n..or to check how strong an association between several words is:\n 'suchenwirth tcl': 57 hits\n 'suchenwirth java': 14 hits\n\nThe numbers may change over time, but the tendency ("fuzzy truth") can at least be estimated.