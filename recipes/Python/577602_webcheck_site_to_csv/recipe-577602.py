from __future__ import with_statement

import csv
import os

# this module is included as part of webcheck.
import serialize

FILENAME = 'my_site_links_as_csv.csv'
DATFILE = 'my_site/webcheck.dat'

if __name__ == '__main__':

    # using webcheck's serialize module to create a site object.
    site = serialize.deserialize(open(DATFILE, 'r'))

    with open(FILENAME, 'w') as sitecsv:
        writer = csv.writer(sitecsv)

        writer.writerow(("path", "extension", "internal", "errors"))
        writer.writerows(
                ((k,
                 os.path.splitext(v.path)[-1],
                 v.isinternal,
                 ' '.join(v.linkproblems))
                 
                 # the site object has a dictionary between URI and a link object.
                 for (k, v) in site.linkMap.iteritems()))
