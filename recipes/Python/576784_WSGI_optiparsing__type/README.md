## WSGI option parsing & type conversion

Originally published: 2009-05-28 16:29:06
Last updated: 2009-05-28 16:32:11
Author: Brendan O'Connor

fetches named parameters from the WSGI querystring, plus defaults for missing values, and type conversions so you dont accidentally have strings when you want numbers.