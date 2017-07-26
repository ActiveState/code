###Misspell words to avoid detection

Originally published: 2005-09-06 08:32:25
Last updated: 2005-09-06 15:39:26
Author: Robert McDermott

The misspell class takes a string and slightly mangles it by randomly transposing two adjacent characters while leaving the first and last characters intact. The resulting text is almost completely misspelled but still completely readable. Words less than four characters, numbers, email addresses and URLs are untouched. Each run will produce a message with a different signature (checksum).