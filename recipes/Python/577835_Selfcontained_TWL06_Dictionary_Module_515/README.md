## Self-contained TWL06 Dictionary Module (515 KB)  
Originally published: 2011-08-10 14:24:05  
Last updated: 2011-08-10 20:32:03  
Author: Michael Fogleman  
  
A convenient, self-contained, 515 KB Scrabble dictionary module, ideal
for use in word games.

Functionality:

- Check if a word is in the dictionary.
- Enumerate all words in the dictionary.
- Determine what letters may appear after a given prefix.
- Determine what words can be formed by anagramming a set of letters.

Sample usage:

>>> import twl
>>> twl.check('dog')
True
>>> twl.check('dgo')
False
>>> words = set(twl.iterator())
>>> len(words)
178691
>>> twl.children('dude')
['$', 'd', 'e', 's']
>>> list(twl.anagram('top'))
['op', 'opt', 'pot', 'to', 'top']