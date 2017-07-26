## Recursive find and replace in all files in directory with regex 
Originally published: 2012-11-01 12:43:16 
Last updated: 2013-03-21 12:33:44 
Author: ccpizza  
 
Search and replace files recursively in a given directory. Accepts regular expressions as search and replacement patterns.\n\n**Example usage**:\n\n    python find_replace_regex.py ".", "<span[^>]*>", "<div>", "*.html" backup\n\n**Note**:\nOn win32 the `<` and `>` symbols are interpreted by the shell as input/output redirection even when they are surrounded with single or double quotes, and therefore need to be escaped with the caret character `^`.