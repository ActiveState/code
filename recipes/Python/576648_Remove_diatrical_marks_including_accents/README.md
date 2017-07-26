###Remove diatrical marks (including accents) from strings using latin alphabets

Originally published: 2009-02-10 12:21:26
Last updated: 2009-02-11 11:40:55
Author: Sylvain Fourmanoit

Many written languages using latin alphabets employ [diacritical marks](http://en.wikipedia.org/wiki/Diacritic). Even today, it is still pretty common to encounter situations where it would be desirable to get rid of them: files naming, creation of easy to read URIs, indexing schemes, etc. \n\nAn easy way has always been to simply filter out any "decorated characters"; unfortunately, this does not preserve the base, undecorated glyphs. But thanks to Unicode support in Python, it is now straightforward to perform such a transliteration.\n\n(This recipe was completely rewritten based on a comment by Mathieu Clabaut: many thanks to him!)