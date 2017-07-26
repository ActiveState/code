import string, urllib, re, os, exceptions

JUST_THE_US = 0

class CityNotFound(exceptions.Exception):
    pass

def xerox_parc_url(marklist):
    avg_lat, avg_lon = max_lat, max_lon = marklist[0]
    marks = "%f,%f" % marklist[0]
    for lat, lon in marklist[1:]:
        marks = marks + ";%f,%f" % (lat, lon)
        avg_lat = avg_lat + lat
        avg_lon = avg_lon + lon
        if lat > max_lat: max_lat = lat
        if lon > max_lon: max_lon = lon
    avg_lat = avg_lat / len(marklist)
    avg_lon = avg_lon / len(marklist)
    if len(marklist) == 1:
        max_lat, max_lon = avg_lat + 1, avg_lon + 1
    diff = max(max_lat - avg_lat, max_lon - avg_lon)
    D = {'height': 4 * diff,
         'width': 4 * diff,
         'lat': avg_lat, 'lon': avg_lon,
         'marks': marks}
    if JUST_THE_US:
        url = ("http://pubweb.parc.xerox.com/map/db=usa/ht=%(height)f" +
               "/wd=%(width)f/color=1/mark=%(marks)s/lat=%(lat)f/" +
               "lon=%(lon)f/") % D
    else:
        url = ("http://pubweb.parc.xerox.com/map/color=1/ht=%(height)f" +
               "/wd=%(width)f/color=1/mark=%(marks)s/lat=%(lat)f/" +
               "lon=%(lon)f/") % D
    return url

"""Presumably the intent of the cookbook is largely educational. I should
therefore illuminate something I did really pretty badly in this function.
Notice the ridiculous clumsiness of the "for x in inf.readlines()" loop,
which is utterly and stupidly dependent upon the specific format of the
HTML page returned by the www.astro.ch site. If that format ever changes,
the function breaks. If I had been clever and used htmllib.HTMLParser, I
might have been a bit more immune to modest format changes. If my motivation
persists, I might take a stab at that. No promises."""

def findcity(city, state):
    Please_click = re.compile("Please click")
    city_re = re.compile(city)
    state_re = re.compile(state)
    url = ("""http://www.astro.ch/cgi-bin/atlw3/aq.cgi?expr=%s&lang=e"""
           % (string.replace(city, " ", "+") + "%2C+" + state))
    lst = [ ]
    found_please_click = 0
    inf = urllib.FancyURLopener().open(url)
    for x in inf.readlines():
        x = x[:-1]
        if Please_click.search(x) != None:
            # here is one assumption about unchanging structure
            found_please_click = 1
        if (city_re.search(x) != None and
            state_re.search(x) != None and
            found_please_click):
            # pick apart the HTML pieces
            L = [ ]
            for y in string.split(x, '<'):
                L = L + string.split(y, '>')
            # discard any pieces of zero length
            L = filter(lambda x: len(x) > 0, L)
            lst.append(L)
    inf.close()
    try:
        # here's another few assumptions
        x = lst[0]
        lat, lon = x[6], x[10]
    except IndexError:
        raise CityNotFound
    def getdegrees(x, dividers):
        def myeval(x):
            if len(x) == 2 and x[0] == "0":
                return eval(x[1])
            return eval(x)
        if string.count(x, dividers[0]):
            x = map(myeval, string.split(x, dividers[0]))
            return x[0] + (x[1] / 60.)
        elif string.count(x, dividers[1]):
            x = map(myeval, string.split(x, dividers[1]))
            return -(x[0] + (x[1] / 60.))
        else:
            raise "Bogus result", x
    return getdegrees(lat, "ns"), getdegrees(lon, "ew")

def showcities(citylist):
    marklist = [ ]
    for city, state in citylist:
        try:
            lat, lon = findcity(city, state)
            print ("%s, %s:" % (city, state)), lat, lon
            marklist.append((lat, lon))
        except CityNotFound:
            print "%s, %s: not in database?" % (city, state)
    url = xerox_parc_url(marklist)
    # print url
    os.system('netscape "%s"' % url)

citylist = (("Natick", "MA"),
            ("Rhinebeck", "NY"),
            ("New Haven", "CT"),
            ("King of Prussia", "PA"))

citylist1 = (("Mexico City", "Mexico"),
             ("Acapulco", "Mexico"),
             ("Abilene", "Texas"),
             ("Tulum", "Mexico"))

citylist2 = (("Munich", "Germany"),
             ("London", "England"),
             ("Madrid", "Spain"),
             ("Paris", "France"))

showcities(citylist1)
