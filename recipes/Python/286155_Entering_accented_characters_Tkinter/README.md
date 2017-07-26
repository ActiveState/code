## Entering accented characters in Tkinter widgets

Originally published: 2004-06-19 02:09:47
Last updated: 2005-01-12 22:00:07
Author: Artur de Sousa Rocha

This module provides two standard Tkinter widgets, Entry and ScrolledText, modified for text editing with key bindings that allow entering accented letters, umlauts, etc.\n\nUsage: To enter an accented character, press Ctrl-symbol, then press the character key. Example: to enter U with umlaut, press Ctrl-", U. For accent symbols that need shift, press Ctrl-Shift-symbol (for example, Ctrl-Shift-' if " is under Shift-').\n\nAccent bindings are defined in the Diacritical.accent table. Not all accents exist on all letters. This is handled by gracefully falling back to the base letter.\n\nAdditional changes in default Tk key bindings: Ctrl-A is now select-all.