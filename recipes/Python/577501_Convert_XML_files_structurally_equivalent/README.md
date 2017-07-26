## Convert XML files to structurally equivalent garbage

Originally published: 2010-12-15 18:57:41
Last updated: 2010-12-15 18:57:42
Author: Eric Promislow

You've found a bug in an application that reads XML files.  You'd prefer not to share your data, though, but you'd really like to help the vendor fix the bug.  This program maintains the document's structure, but it randonly converts each word into random gibberish, replacing vowels with vowels, consonants with consonants, and digits with digits.  It also interns each element and attribute name, so all instances of "foo" as an element or attribute name would show up as, say, "xeu", but instances of "foo" in character data would be mapped to a different string each time.