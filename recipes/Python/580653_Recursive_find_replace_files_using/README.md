## Recursive find replace in files using regex  
Originally published: 2016-04-26 18:34:30  
Last updated: 2016-04-28 13:24:15  
Author: ccpizza   
  
Recursively find and replace text in files under a specific folder with preview of changed data in dry-run mode
============

Example Usage
---------------

**See what is going to change (dry run):**

    find_replace.py --dir project/myfolder --search-regex "\d{4}-\d{2}-\d{2}" --replace-regex "2012-12-12" --dryrun

**Do actual replacement:**

    find_replace.py --dir project/myfolder --search-regex "\d{4}-\d{2}-\d{2}" --replace-regex "2012-12-12"

**Do actual replacement and create backup files:**

    find_replace.py --dir project/myfolder --search-regex "\d{4}-\d{2}-\d{2}" --replace-regex "2012-12-12" --create-backup


**Same action as previous command with short-hand syntax:**

    find_replace.py -d project/myfolder -s "\d{4}-\d{2}-\d{2}" -r "2012-12-12" -b

Output of `find_replace.py -h`:

    DESCRIPTION:
        Find and replace recursively from the given folder using regular expressions
    
    optional arguments:
      -h, --help            show this help message and exit
      --dir DIR, -d DIR     folder to search in; by default current folder
      --search-regex SEARCH_REGEX, -s SEARCH_REGEX
                            search regex
      --replace-regex REPLACE_REGEX, -r REPLACE_REGEX
                            replacement regex
      --glob GLOB, -g GLOB  glob pattern, i.e. *.html
      --dryrun, -dr         don't replace anything just show what is going to be
                            done
      --create-backup, -b   Create backup files
    
    USAGE:
       find_replace.py -d [my_folder] -s <search_regex> -r <replace_regex> -g [glob_pattern]
