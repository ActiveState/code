#!/usr/bin/env python

import urlparse
import urllib2
import os
import HTMLParser
import sre

class HTMLLinkScanner(HTMLParser.HTMLParser):
  tags = {'a':'href','img':'src','frame':'src','base':'href'}

  def reset(self):
    self.links = {}
    self.replacements = []
    HTMLParser.HTMLParser.reset(self)

  def handle_starttag(self, tag, attrs):
    if tag in self.tags:
      checkattrs = self.tags[tag]
      if isinstance(checkattrs, (str, unicode)):
        checkattrs = [checkattrs]
      for attr, value in attrs:
        if attr in checkattrs:
          if tag != 'base':
            link = urlparse.urldefrag(value)[0]
            self.links[link] = True
          self.replacements.append((self.get_starttag_text(), attr, value))

class MirrorRetriever:
  def __init__(self, archivedir):
    self.archivedir = archivedir
    self.urlmap = {}

  def url2filename(self, url):
    scheme, location, path, query, fragment = urlparse.urlsplit(url)
    if not path or path.endswith('/'):
      path += 'index.html'
    path = os.path.join(*path.split('/'))
    if scheme.lower() != 'http':
      location = os.path.join(scheme, location)
    # ignore query for the meantime
    return os.path.join(self.archivedir, location, path)

  def testinclude(self, url):
    scheme, location, path, query, fragment = urlparse.urlsplit(url)
    if scheme in ('mailto', 'javascript'): return False
    # TODO: add ability to specify site
    # return location.lower() == 'www.mcmillan-inc.com'
    return True

  def ensuredir(self, pathname):
    if not os.path.isdir(pathname):
      self.ensuredir(os.path.dirname(pathname))
      os.mkdir(pathname)

  def retrieveurl(self, url):
    return urllib2.urlopen(url).read()

  def mirror(self, url):
    if url in self.urlmap:
      return
    else:
      filename = self.url2filename(url)
      if not self.testinclude(url):
        return
      print url,'->',filename
      self.urlmap[url] = filename
      # TODO: add an option about re-reading stuff
      if os.path.isfile(filename):
        contents = open(filename, 'r').read()
      else:
        try:
          contents = self.retrieveurl(url)
        except urllib2.URLError, e:
          print 'could not retrieve url %s: %s' % (url, e)
          return
      self.ensuredir(os.path.dirname(filename))
      linkscanner = HTMLLinkScanner()
      try:
        linkscanner.feed(contents)
      except:
        print 'could not parse %s as html' % url
      linkstomirror = []
      for link in linkscanner.links:
        linkurl = urlparse.urljoin(url, link)
        linkstomirror.append(linkurl)
      contents = sre.sub('http://web.archive.org/web/[0-9]{14}/', '', contents)
      for tagtext, attr, link in linkscanner.replacements:
        scheme, location, path, query, fragment = urlparse.urlsplit(link)
        newtext = None
        if tagtext.lower().startswith('<base'):
          # strip out base references
          newtext = ''
        elif scheme or location:
          if not self.testinclude(link): continue
          linkfilename = self.url2filename(link)
          newtext = tagtext.replace(link, 'file://%s' % linkfilename)
        elif path.startswith('/'):
          linkurl = urlparse.urljoin(url, link)
          linkfilename = self.url2filename(linkurl)
          newtext = tagtext.replace(link, 'file://%s' % linkfilename)
        if newtext is not None:
          contents = contents.replace(tagtext, newtext)
      contentsfile = open(filename, 'w')
      contentsfile.write(contents)
      contentsfile.close()
      for linkurl in linkstomirror:
        self.mirror(linkurl)

class WaybackRetriever(MirrorRetriever):
  def __init__(self, archivedir, datestring):
    MirrorRetriever.__init__(self, archivedir)
    self.datestring = datestring

  def retrieveurl(self, url):
    waybackurl = 'http://web.archive.org/web/%s/%s' % (self.datestring, url)
    contents = urllib2.urlopen(waybackurl).read()
    if contents.find("Sorry, we can't find the archived version of this page") != -1:
      raise urllib2.URLError("not in wayback archive")
    # remove the copyrighted javascript from the wayback machine...
    contents = sre.sub('\\<SCRIPT language="Javascript"\\>(.|\r|\n)*(// FILE ARCHIVED ON [0-9]{14} AND RETRIEVED(.|\r|\n)* ON [0-9]{14}[.])(.|\r|\n)*\\</SCRIPT\\>', '\\2', contents)
    # replace the javascript-style comments indicating the retrieval with html comments
    contents = sre.sub('// ((FILE|INTERNET).*)', '<!-- \\1 -->', contents)
    return contents

if __name__ == '__main__':
  import sys
  m = WaybackRetriever(os.path.abspath('.'), sys.argv[2])
  m.mirror(sys.argv[1])
