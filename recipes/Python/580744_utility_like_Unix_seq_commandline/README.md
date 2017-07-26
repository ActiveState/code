## A utility like Unix seq (command-line), in Python

Originally published: 2017-01-08 17:48:56
Last updated: 2017-01-08 17:48:57
Author: Vasudev Ram

\nThis recipe shows how to create a utility like Unix seq (command-line), in Python.\nseq is described here: \n\nhttps://en.wikipedia.org/wiki/Seq_(Unix)\n\nbut briefly, it is a command-line utility that takes 1 to 3 arguments (some being optional), the start, stop and step, and prints numbers from the start value to the stop value, on standard output. So seq has many uses in bigger commands or scripts; a common category of use is to quickly generate multiple filenames or other strings that contain numbers in them, for exhaustive testing, load testing or other purposes. A similar command called jot is found on some Unix systems.\n\nThis recipe does not try to be exactly the same in functionality as seq. It has some differences. However the core functionality of generating integer sequences is the same (but without steps other than 1 for the range).\n\nMore details and sample output are here:\n\nhttps://jugad2.blogspot.in/2017/01/an-unix-seq-like-utility-in-python.html\n\nThe code is below.\n