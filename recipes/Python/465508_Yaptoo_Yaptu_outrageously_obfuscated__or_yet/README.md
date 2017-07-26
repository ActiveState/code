## Yaptoo (Yaptu outrageously obfuscated) - or yet yet another templating utility 
Originally published: 2005-12-27 10:19:59 
Last updated: 2006-11-15 16:58:11 
Author: Michael Palmer 
 
An enhanced version of yaptu, with the following changes\n- separated parsing from execution\n- added caching of parsed templates\n- added some error reporting\n- added a choice of template syntaxes\n- added comment syntax\n- added Cheetah-style variable substitution with optional caching of the equivalent Python expression\n- limited flow control to 'for' and 'if'\nReasonably small, no external dependencies, pretty fast.