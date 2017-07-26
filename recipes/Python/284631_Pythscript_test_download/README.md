###A Python script to test download mirrors

Originally published: 2004-05-18 12:45:48
Last updated: 2004-05-19 21:28:55
Author: Tim Lesher

Bandwidth testing is easy with Python's built-in web access, HTML parsing, and threading modules.\n\nWhen Fedora Core 2 was released, I wanted to find which download mirror would be fastest when I tried downloading the CD images.  It only took about an hour to whip up this mirror bandwidth tester.\n\nThis script demonstrates web download, HTML parsing, and some interesting threading issues.