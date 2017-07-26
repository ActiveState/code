# -*- coding: utf-8 -*-

"""Wordze.com API python bindings."""

__all__ = ("Api", "ApiError", "HistoryKeyword", "Keyword",
           "history", "search", "status", "single")

import urllib
import urllib2
import urlparse
from functools import wraps, partial
from datetime import datetime
from xml.dom.minidom import Element, parse

# Search filters
F_NONE = 1
F_ADULT = 2
F_DRUGS = 3
F_GAMBLING = 4
F_WAREZ_HACKING = 5
F_ALL = 6

# Search styles
S_EXACT = "exact"
S_BROAD = "broad"
S_ANY = "any"


def extract_text(dom, name, wrapper=None):
    """
    Function tries to extract text data from the first tag
    with a given name and wrapps it in a give function / class.
    """
    elements = dom.getElementsByTagName(name)
    if elements:
        text = elements[0].lastChild.data
    else:
        text = ""
    return wrapper(text) if wrapper else text


class ApiError(Exception):
    """Api error wrapper."""


class Keyword(dict):
    """Class wrapper for a keyword item."""

    def __init__(self, data):
        """Constructor."""
        if isinstance(data, Element):
            self["count"] = int(data.getAttribute("Count"))
            self["estimated"] = int(data.getAttribute("Estimated"))
            # FIXME: ugly
            if "term" not in self:
                self["term"] = data.childNodes[0].data
        else:
            self["count"], self["estimated"] = None
            self["term"] = data

    def __repr__(self):
        return "\"%s\"" % self["term"].encode("utf-8")

    def __cmp__(self, other):
        if not isinstance(other, Keyword):
            raise TypeError

        if self["count"] < other["count"]:
            return -1
        elif self["count"] == other["count"]:
            return 0
        else:
            return 1


class HistoryKeyword(Keyword):
    """Class wrapper for a keyword item from history search."""

    def __init__(self, term, history):
        self["term"] = term
        self["date"] = datetime.strptime(
            history.getAttribute("Date"), "%Y-%m-%d")
        super(HistoryKeyword, self).__init__(history)

    def __repr__(self):
        return "%s on %s" % (super(HistoryKeyword, self).__repr__(),
                             self["date"].date())

class Api(object):
    """Api worker class."""

    def __init__(self, apikey):
        """Constructor."""
        self.apikey = apikey
        self.apiurl = "http://api.wordze.com"

    def history(self, query, date):
        """
        Method performs a lookup of the history for a given
        keyword.

        Note: the date should be either datetime.datetime
        instance or a string of format YYYYMM.
        """
        if isinstance(date, datetime):
            date = date.strftime("%Y%m")
        elif isinstance(date, basestring):
            try:
                # Validating date format
                datetime.strptime(date, "%Y%m")
            except ValueError:
                raise ApiError("Invalid date format")
        else:
            raise ApiError("Invalid date format")

        dom = parse(self._request("ApiHistory", {"ApiKey": self.apikey,
                                                 "Query": query,
                                                 "Date": date}))
        if self._validate(dom):
            # We have just one query, which doesn't change,
            # from item to item, so it's convinient to
            # wrap it in a partial.
            _HistoryKeyword = partial(HistoryKeyword, query)
            keywords = map(_HistoryKeyword(query),
                           dom.getElementsByTagName("data"))
            return keywords

    def status(self):
        """
        Method checks Wordze.com account status (number of API
        queries used for a day).

        Note: You should ONLY run this at the start of your
        application, and keep track until it completes.
        """
        dom = parse(self._request("AccountStatus",
                                  {"ApiKey": self.apikey}))
        if self._validate(dom):
            return {"Search": extract_text(dom, "Search"),
                    "Wordrank": extract_text(dom, "Wordrank"),
                    "Dig": extract_text(dom, "Dig")}
        return {}

    def single(self, *queries):
        """
        Method performs a a single keyword search for a given list
        of keywords.
        """
        if len(queries) > 500:
            raise ApiError("Single keyword search is limited to "
                           "500 queries at a time")

        dom = parse(
            self._request("KeywordSingle", {"ApiKey": self.apikey,
                                            "Query": ",".join(queries)}))
        if self._validate(dom):
            return sorted(map(Keyword, dom.getElementsByTagName("Keyword")))

    def search(self,
               query, pagenum=1, filtertype=F_NONE, numresult=20,
               searchstyle=S_BROAD, charlen=None, countlim=None):
        """
        Method performs a search using Wordze.com API.

        Availible extraparams:
        * query - keyword to search for
        * pagenum - whe page number in results to show
        * filtertype - what to filter out, should be one of the F_* constants
        * numresult - number of results per page
        * searchstyle - should be one of the S_* constants
        * charlen - keyword length limit, explanation:
            charlen=-15 will only produce results with 15 or less
                    characters in the keyword
            charlen=25 will only produce results with 25 or more
                    characters in the keyword.

          Note that, length is calculated __including__ spaces.
        * countlim - keyword hit count limit , explanation:
           countlim=-15 will only produce results with 15 or less hits
           countlim=100 will only produce results with 100 or more hits

        TODO: write this as a generator yielding pages one by one,
              until there's nothing availible
        """
        # This is ugly, but well, entitled keyword arguments in a
        # function call are even uglier.
        params = {"ApiKey": self.apikey,
                  "Query": query,
                  "PageNum": pagenum,
                  "FilterType": filtertype,
                  "NumResult": numresult,
                  "SearchStyle": searchstyle,
                  "CharLen": charlen,
                  "CountLim": countlim}

        dom = parse(self._request("ApiSearch", params))
        if self._validate(dom):
            print dom.toxml()
            return {
                "page": extract_text(dom, "Page", int),
                "total": extract_text(dom, "TotalPages", int),
                "searchstyle": extract_text(dom, "SearchStyle"),
                "filters": extract_text(dom, "Filters", int),
                "numresult": extract_text(dom, "ResultsPerPage", int),
                "keywords": sorted(map(Keyword,
                                       dom.getElementsByTagName("Keyword")))}

    def _request(self, method, params, count=None):
        url = urlparse.urljoin(
            self.apiurl, "%s?%s" % (method, urllib.urlencode(params)))

        # XXX: just in case anyone supplies a negative
        # max count value :)
        count = count if count > 0 else None
        while count != 0:
            if count:
                count -= 1

            try:
                request = urllib2.urlopen(url)
            except urllib2.URLError, exc:
                print "%s...retrying" % exc
            else:
                return request

    def _validate(self, dom):
        """
        Method validates API response, wrapped in minidom constructor.
        If there are errors present, ApiError with appropriate error
        message is raised.
        """
        errors = dom.getElementsByTagName("Error")
        if errors:
            raise ApiError(", ".join(error.lastChild.data for error in errors))
        return True


# Shortcut functions
apiworker = None

def configure(apikey):
    """Function sets the Api worker for the global (module) calls."""
    global apiworker
    apiworker = Api(apikey)

def proxy(obj, attr):
    @wraps(getattr(Api, attr))
    def wrapper(*args, **kw):
        global apiworker
        if apiworker:
            return getattr(apiworker, attr)(*args, **kw)
        raise ApiError("ApiKey not set")
    return wrapper

search = proxy(apiworker, "search")
status = proxy(apiworker, "status")
single = proxy(apiworker, "single")
history = proxy(apiworker, "history")
