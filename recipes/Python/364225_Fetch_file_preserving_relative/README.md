## Fetch a file preserving relative path

Originally published: 2005-01-23 04:41:42
Last updated: 2005-01-23 04:41:42
Author: Artur de Sousa Rocha

The fetch_relative() function downloads a file, reproducing the directory structure from the server. After downloading, additional callback function can be performed on the file's contents. If the local copy already exists, the file is not re-refetched, and the callback is performed on the local copy.