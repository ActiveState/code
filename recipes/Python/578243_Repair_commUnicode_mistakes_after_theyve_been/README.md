###Repair common Unicode mistakes after they've been made (obsoleted by ftfy package)

Originally published: 2012-08-17 17:30:22
Last updated: 2016-09-28 02:33:32
Author: Rob Speer

Something you will find all over the place, in real-world text, is text that's encoded as UTF-8, decoded in some ugly format like Latin-1 or even Windows codepage 1252, and mistakenly encoded as UTF-8 again.\n\nThis causes your perfectly good Unicode-aware code to end up with garbage text because someone else (or maybe "someone else") made a mistake.\n\nThis function looks for the evidence of that having happened and fixes it. It determines whether it should replace nonsense sequences of single-byte characters that were really meant to be UTF-8 characters, and if so, turns them into the correctly-encoded Unicode character that they were meant to represent.\n