###Pick random elements from a predefined list of choices

Originally published: 2011-06-14 17:40:31
Last updated: 2011-06-14 17:46:41
Author: Patrick Dobbs

This (quick but strangely satisfying) recipe combines the use of random.choice with functools.partial from the standard library. It is a factory function returning random.choice pre-filled with its sequence of options.\n