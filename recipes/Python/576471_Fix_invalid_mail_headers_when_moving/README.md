###Fix invalid mail headers when moving from Thunderbird to IMAP

Originally published: 2008-08-30 20:08:02
Last updated: 2008-08-30 20:08:02
Author: Krys Wilken

Removes ">From" and "From " lines from mail headers.\n\nThunderbird adds invalid mail headers to it's local folders.  Cyrus IMAP is strict about them.  This script walks through all files in the given directories and removes any line that starts with ">From" or "From " (note the space and no colon).\n\nRequires Python 2.5+.\n