## Yaptoo (Yaptu outrageously obfuscated) - or yet yet another templating utility  
Originally published: 2005-12-27 10:19:59  
Last updated: 2006-11-15 16:58:11  
Author: Michael Palmer  
  
An enhanced version of yaptu, with the following changes
- separated parsing from execution
- added caching of parsed templates
- added some error reporting
- added a choice of template syntaxes
- added comment syntax
- added Cheetah-style variable substitution with optional caching of the equivalent Python expression
- limited flow control to 'for' and 'if'
Reasonably small, no external dependencies, pretty fast.