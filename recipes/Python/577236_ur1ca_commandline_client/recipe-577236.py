#!/usr/bin/env python
"""ur1.py -- command-line ur1.ca client.

ur1.ca is the URL shortening services provided by status.net. This script
makes it possible to access the service from the command line. This is done
by scraping the returned page and look for the shortened URL.

USAGE:
    ur1.py LONGURL

RETURN STATUS:
    If the URL is succesfully shortened by ur1.ca, it is written
    to the standard output, and the program exits with status 0.

    If ur1.ca fails to shorten the long URL, the error message
    provided by ur1.ca is written to the standard error, and the
    program exits with status 1.

    If the input URL is malformed, no attempts of contacting the
    server is made, and the program exits with status 2.

"""


import sys
import urllib
import urlparse
import re


UR1CA = "http://ur1.ca/"
ESUCCESS = 0
EFAIL = 1
EBADARG = 2
RE_GOOD = re.compile(r'<p class="success">Your ur1 is: <a href="(?P<shorturl>.+)">(?P=shorturl)</a></p>')
RE_BAD = re.compile(r'<p class="error">(?P<errormsg>.+)</p>')


def isgoodarg(url):
    """Check if the input URL makes "sense".

    A URL does not make sense if the scheme is neither http or https,
    or the host part is missing.

    url: input URL

    Returns boolean indicating whether the URL makes sense.

    """
    parse_result = urlparse.urlparse(url)
    #pylint: disable-msg=E1101
    isgoodscheme = (parse_result.scheme == "http" or
            parse_result.scheme == "https")
    isgoodhost = parse_result.hostname
    return isgoodscheme and isgoodhost


def parameterize(url):
    """Encode input URL as POST parameter.

    url: a string which is the URL to be passed to ur1.ca service.

    Returns the POST parameter constructed from the URL.

    """
    return urllib.urlencode({"longurl": url})


def request(parameter):
    """Send POST request to ur1.ca using the parameter.

    parameter: the parameter to the POST request, as returned by
    parameterize().

    Returns the file-like object as returned by urllib.urlopen.

    """
    return urllib.urlopen(UR1CA, parameter)


def retrievedoc(response):
    """Retrieve the HTML text from the ur1.ca response.

    response: the file-like HTTP response file returned by ur1.ca.

    Returns the text as a string.

    """
    #XXX: ensure all bytes are read
    res_info = response.info()
    clength = int(res_info["content-length"])
    return response.read(clength)


def scrape(document):
    """Scrape the HTML document returned from ur1.ca for the answer.

    document: HTML document returned from ur1.ca

    Returns a 2-tuple (success, answer) where --

    success: boolean value indicating whether the service returned
    some meaningful result

    answer: if success, this is the shortened URL, otherwise a string
    indicating the possible problem

    """
    goodguess = RE_GOOD.search(document)
    if goodguess:
        matchdict = goodguess.groupdict()
        return (True, matchdict["shorturl"])
    badguess = RE_BAD.search(document)
    if badguess:
        matchdict = badguess.groupdict()
        return (False, matchdict["errormsg"])
    else:
        return (False, "Unknown local error.")


def __do_main():
    """Do everything."""

    try:
        arg = sys.argv[1]
    except IndexError:
        sys.exit(EBADARG)
    if not isgoodarg(arg):
        sys.exit(EBADARG)

    post_param = parameterize(arg)
    answerfile = request(post_param)
    doc = retrievedoc(answerfile)
    answerfile.close()
    status, msg = scrape(doc)

    if status:
        print msg
        sys.exit(ESUCCESS)
    else:
        print >> sys.stderr, msg
        sys.exit(EFAIL)


if __name__ == "__main__":
    __do_main()
