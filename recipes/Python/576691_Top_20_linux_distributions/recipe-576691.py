import urllib2
import re
import time

def LinuxDistros():
  req = urllib2.Request("http://lwn.net/Distributions/")
  f = urllib2.urlopen(req)
  t = f.read()
  f.close()
  rc = re.compile('<li> <b><a href.*>(.*)</a></b><br>')
  return rc.findall(t)

def DistroRank(nix):
  enc = "http://search.yahoo.com/search?p="+urllib2.quote('"'+nix+'" "linux distribution"')
  req = urllib2.Request(enc)
  req.add_header('User-Agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8) Gecko/20051111 Firefox/1.5 BAVM/1.0.0')
  f = urllib2.urlopen(req)
  t = f.read()
  f.close()
  rc = re.compile('<span id="infotext">1 - 10 of (.*) for <strong>')
  rez = rc.search(t)
  if rez:
    return int(rez.groups()[0].replace(',',''))
  else:
    return 0

def TopDistros():
  print 'Fetching ranks from search engine...'
  distros = LinuxDistros()
  res = []
  for d in distros:
    res.append((DistroRank(d),d))
    print 'Fetched', len(res),'distro of',len(distros)
    time.sleep(2)
  res = sorted(res,reverse=True)[:20]
  total = sum(r for r,d in res)
  res = [(round(100.*r/total,2), d) for r,d in res]
  print '-'*20
  print 'Distro  Rating(%)'
  print '-'*20
  for r,d in res:
    print d,r

TopDistros()
