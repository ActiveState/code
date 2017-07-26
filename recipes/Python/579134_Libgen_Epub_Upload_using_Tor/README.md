###Libgen Epub Upload using Tor

Originally published: 2015-12-06 19:21:49
Last updated: 2015-12-06 19:23:54
Author: fuji239 

This script shows how to upload epub files in Library Genesys (libgen) automatically by using Tor. Please note that only copyright free epubs should be used (such as those present in https://www.gutenberg.org/). \nIt will also check if MD5 hash is present before uploading.\nThis is provided for python educative purposes only : it shows how to use a Tor proxy, Mechanize (for uploading and form processing), Hashlib for MD5 calculation, Filemagic for mimetype detecting and BeautifulSoup for response analyzing, all together.