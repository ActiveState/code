## sed/awk : Python script to rename subdirectories of a directory tree, replace strings in files  
Originally published: 2005-07-05 12:33:51  
Last updated: 2005-07-05 12:33:51  
Author: Bibha Tripathi  
  
I needed to write a sed/awk Python equivalent for walking into a directory tree and renaming certain subdirectories, while also looking into all xml files on the way and replacing/modifying certain strings in those files.

It would be nicer if someone could suggest an enhanced re.sub(regex, replacement, subject) where I could replace all strings of a certain pattern with other strings of a certain pattern i.e. the second argument in re.sub namely 'replacement' would then be a regular expression and would be a different string for each different string in 'subject' that matches with the pattern 'regex'. For example 'arthinternational-d' would be replaced by 'arthinternational-r', 'arthfmt-d' would be replaced by 'arthfmt-r' but 'a-d' would remain unmodified.