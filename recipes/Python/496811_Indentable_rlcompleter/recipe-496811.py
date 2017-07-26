"""Indentable rlcompleter

Extend standard rlcompleter module to let tab key can indent
and also completing valid Python identifiers and keywords."""

import readline,rlcompleter

class irlcompleter(rlcompleter.Completer):
        def complete(self, text, state):
                if text == "":
                        readline.insert_text('\t')
                        return None
                else:
                        return rlcompleter.Completer.complete(self,text,state)

#you could change this line to bind another key instead tab.
readline.parse_and_bind("tab: complete")
readline.set_completer(irlcompleter().complete)
