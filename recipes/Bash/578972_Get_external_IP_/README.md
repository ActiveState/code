## Get external IP & geolocation in bash.

Originally published: 2014-11-30 00:37:29
Last updated: 2014-11-30 00:46:28
Author: manu 

Very simple way to get external IP and geolocation uysing dig and geoiplookup.\n\n`dig` is cool to obtain my external IP and I use `geoiplookup` to convert IP to location. You need geoip-bin and, geoip-database (and/or geoip-database-contrib and geoip-database-extra). In Debian, database seems update monthly.\n\nIt's just a tip.