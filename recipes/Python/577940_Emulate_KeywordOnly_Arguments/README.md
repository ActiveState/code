## Emulate Keyword-Only Arguments in Python 2

Originally published: 2011-11-03 01:04:13
Last updated: 2011-11-03 18:31:52
Author: Eric Snow

Python 3 introduced a useful feature: keyword-only arguments.  In order to get the same effect in Python 2, you must use **kwargs in your parameter list.  Then, at the beginning of your function body you must manually extract what would be the keyword-only arguments once you upgrade to 3.\n\nThis recipe helps reduce the boilerplate to a single function call.  You still don't get those parameters in your "def" clause (where they are more obvious), but at least it reduces the clutter.