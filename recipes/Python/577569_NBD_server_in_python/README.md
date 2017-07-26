###NBD server in python

Originally published: 2011-02-08 20:59:22
Last updated: 2011-02-08 20:59:23
Author: Dima Tisnek

Linux Network Block Device server in Python\n\nThis is a simplified version based on Kragen Sitaker's http://lists.canonical.org/pipermail/kragen-hacks/2004-May/000397.html\n\nClose is never actually called, at least not on the same connection -- linux C nbd-client -d seems to stall, perhaps it tries to open another socket?\n\nThis code doesn't check for error conditions, failed reads/writes, past end of disk, etc.\n\nIt prints io requests, you can analyze filesystem and user program io patterns.