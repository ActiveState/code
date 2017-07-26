## string multi-partitioning

Originally published: 2010-01-21 18:01:34
Last updated: 2010-03-26 20:03:59
Author: Michael Grünewald

Works like the `partition` method of strings in Python2.5+, but has support for more than one delimiter.\n\n*Better description by Gabriel Genellina:*\n\n> Split the string at separator boundaries. The separators are searched from left to right, in the same order specified, and one after another. Unlike `partition`, all of them must be present (else `ValueError` is raised). Only one split per separator occurrence is done. Returns a list containing one more element than separators were given: first, text from beginning of the string up to (but not including) the first separator; the first separator itself; text between the first separator and the second one; the second separator; and so on. The last element contains all text following the last separator.