###Latin1 to ASCII -- The UNICODE Hammer

Originally published: 2003-11-10 11:06:49
Last updated: 2003-11-10 11:06:49
Author: Noah Spurrier

latin1_to_ascii -- The UNICODE Hammer -- AKA "The Stupid American"\n\nThis takes a UNICODE string and replaces Latin-1 characters with\nsomething equivalent in 7-bit ASCII and returns a plain ASCII string.\nThis function makes a best effort to convert Latin-1 characters into\nASCII equivalents. It does not just strip out the Latin-1 characters.\nAll characters in the standard 7-bit ASCII range are preserved.\nIn the 8th bit range all the Latin-1 accented letters are converted to\nunaccented equivalents. Most symbol characters are converted to\nsomething meaningful. Anything not converted is deleted.