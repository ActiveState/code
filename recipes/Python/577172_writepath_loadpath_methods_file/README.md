## write_path and load_path methods for file generation scripts

Originally published: 2010-03-31 21:13:03
Last updated: 2010-07-27 06:45:51
Author: Trent Mick

I have a lot of scripts that end up writing files (often build system stuff). Everytime I either end up writing the obvious quick `content = open(path).read()` or I re-implement a function that handles things like: making a backup, some typical logging, encoding support, trying to make it no-op if no changes, etc.\n\nIn this recipe I'll try to add a number of these features so I don't have to keep re-writing this. :) So far this is just a start.\n\nCurrent features:\n\n- rudimentary `encoding` support\n- logging on a given `log` argument\n- `create_backup` argument to create a backup file\n- writes to a temporary file and uses atomic `os.rename` to avoid destroying the existing file if writing fails