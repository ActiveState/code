## xnview backup files remove utility

Originally published: 2010-07-06 17:29:35
Last updated: 2010-07-06 18:09:43
Author: Denis Barmenkov

Currently XnView image viewer (versions up to 1.97.6) correctly rotate images only when option "[x] make backup" set.\n\nBackup files have added name part '.xnbak' before extension:\n\n    original file: IMG0001.jpg\n    backup file: IMG0001.xnbak.jpg\n\nAttached script take a root directory in command line and remove backup files created by XnView only when rotated file present in same directory.