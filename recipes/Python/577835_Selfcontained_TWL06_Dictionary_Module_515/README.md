## Self-contained TWL06 Dictionary Module (515 KB)  
Originally published: 2011-08-10 14:24:05  
Last updated: 2011-08-10 20:32:03  
Author: Michael Fogleman  
  
A convenient, self-contained, 515 KB Scrabble dictionary module, ideal\nfor use in word games.\n\nFunctionality:\n\n- Check if a word is in the dictionary.\n- Enumerate all words in the dictionary.\n- Determine what letters may appear after a given prefix.\n- Determine what words can be formed by anagramming a set of letters.\n\nSample usage:\n\n>>> import twl\n>>> twl.check('dog')\nTrue\n>>> twl.check('dgo')\nFalse\n>>> words = set(twl.iterator())\n>>> len(words)\n178691\n>>> twl.children('dude')\n['$', 'd', 'e', 's']\n>>> list(twl.anagram('top'))\n['op', 'opt', 'pot', 'to', 'top']