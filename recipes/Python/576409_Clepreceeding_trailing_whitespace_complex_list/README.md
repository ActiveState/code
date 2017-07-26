## Clean preceeding and trailing whitespace in complex list dictionary tuple structures  
Originally published: 2008-08-06 15:15:31  
Last updated: 2008-08-06 15:16:54  
Author: Will   
  
Function to clean trailing and or preceeding whitespace from string types in complex list, dictionary, and tuple structures. This is a recursive function to allow for complete coverage of all items in the structure. Wanted to share it as I needed it and after searching for a while I gave up and wrote one.

For example
a = ["\rText  \r\n", "This one is fine", ["stuff ", [" Something Else"], 4, "Another ", "one", " with"], "\twhitespace\r\n"]

print cleanWhiteSpace(a)
Result:
["Text", "This one is fine", ["stuff", ["Something Else"], 4, "Another", "one", "with"], "whitespace"]


