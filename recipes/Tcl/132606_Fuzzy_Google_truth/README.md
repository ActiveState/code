## Fuzzy Google truth  
Originally published: 2002-06-11 15:40:48  
Last updated: 2002-06-11 15:40:48  
Author: andreas kupries  
  
Origin: http://wiki.tcl.tk/3490
Author: Richard Suchenwirth

Given some piece of data where it is doubtful whether they are correct or not, one way to find out is just to ask a search engine like Google, but disregard the results except for the number of found web pages. Chances are that the correct data have a higher hit rate than the faulty one.


Example output in the text widget (asking about a city in Italy, where post code and province were unsure):
 'bellaria rn': 3580 hits
 'bellaria fo': 609 hits
 'bellaria 47814': 1130 hits
 'bellaria 47014': 30 hits

These results seem to indicate that 47814 Bellaria RN (Rimini) is the correct address ;-) On single words one might use this for spelling verification:
 'suchenwirth': 280 hits
 'suchenworth': 0 hits

..or to check how strong an association between several words is:
 'suchenwirth tcl': 57 hits
 'suchenwirth java': 14 hits

The numbers may change over time, but the tendency ("fuzzy truth") can at least be estimated.