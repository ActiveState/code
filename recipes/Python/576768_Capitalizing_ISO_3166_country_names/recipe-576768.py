#!/usr/bin/env python
"""
A small utility library for processing ISO 3166 country codes.

References

ISO 3166 home page URL :-

    http://www.iso.org/iso/country_codes.htm

ISO 3166-1-alpha-2 text file URL :-

    http://www.iso.org/iso/list-en1-semic-3.txt

"""
import os
import urllib2

#-----------------------------------------------------------------------------
def get_lastest_iso3166(filename=None, url=None):
    """
    Retrieves the latest ISO 3166-1 alpha-2 country code text file from the
    iso.org website.

    Saves URL contents to filename. Defaults to the current working directory
    and uses the basename from URL if not specified.

    Assumes the default ISO 3166 URL if not specified.

    """
    #   Pick default URL if not specified.
    if url is None:
        url='http://www.iso.org/iso/list-en1-semic-3.txt'

    print 'downloading %s' % url

    request = urllib2.Request(url)
    response = urllib2.urlopen(request)

    if filename is None:
        save_path = os.path.dirname(__file__)
        basename = os.path.basename(response.geturl())
        filename = os.path.join(save_path, basename)

    fh = open(filename, 'wb')
    fh.write(response.read())
    fh.close()

#-----------------------------------------------------------------------------
def capitalize_country_name(cname):
    """Fixes capitalization edge cases in ISO 3166 country names"""
    #   Replace some non-ASCII character codes with ASCII equivalents.
    cname = cname.replace("\xc9", 'e')
    cname = cname.replace("\xd4", '0')
    cname = cname.replace("\xc5", 'a')

    tokens = [t.capitalize() for t in cname.split()]
    for (i, t) in enumerate(tokens):
        #   General cases.
        if t.upper().startswith('(U.'):
            tokens[i] = t.upper()
        elif t[0] == '(':
            tokens[i] = '(' + t[1:].capitalize()
        elif '-' in t:
            tokens[i] = '-'.join([e.capitalize() for e in t.split('-')])

        #   Some annoying special cases :-)
        if t.lower() in ('of', 'and', 'the', 'former'):
            tokens[i] = t.lower()
        elif t == "D'ivoire":
            tokens[i] = "D'Ivoire"
        elif t == "Mcdonald":
            tokens[i] = "McDonald"
        elif t.upper() == "U.S.":
            tokens[i] = "U.S."

    return ' '.join(tokens)

#-----------------------------------------------------------------------------
def iter_capitalized_iso3166(filename):
    """
    A generator function that parses the free ISO 3166-1 alpha-2 country
    codes text file returning a tuple containing the alpha-2 code and country
    name (in that order).

    Country names are capitalized correctly (taking edge cases into account).

    Example :-

    ('AF', 'Afghanistan')
    ('AX', 'Aland Islands')
    ('AL', 'Albania')
    ('DZ', 'Algeria')
    ('AS', 'American Samoa')
    ...

    References

    ISO 3166 home page URL :-

        http://www.iso.org/iso/country_codes.htm

    ISO 3166-1-alpha-2 text file URL :-

        http://www.iso.org/iso/list-en1-semic-3.txt

    """
    line_count = 0
    for line in open(filename):
        line_count += 1

        if line_count > 2:
            cname, cc = line.strip().split(';')
            yield (cc, capitalize_country_name(cname))

#-----------------------------------------------------------------------------
if __name__ == '__main__':
    get_lastest_iso3166()
    for record in iter_capitalized_iso3166('list-en1-semic-3.txt'):
        print '%s - %s' % record
