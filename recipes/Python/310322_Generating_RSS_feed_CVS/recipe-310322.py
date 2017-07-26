#!/usr/bin/env python
#
# Publish CVS commits to a RSS feed.
#
# This is a Python port of Dave Thomas's commit2rss.rb, because SourceForge
# doesn't support Ruby cvs scripts yet.
#
# To use: checkout your repository's CVSROOT module, edit loginfo, and
# add a line similar to this:
#
#    ALL /path/to/commit2rss.py %{}
# 
# More CVS trigger info at: 
# https://www.cvshome.org/docs/manual/cvs-1.11.17/cvs_18.html#SEC167
# 
# Copyright (c) 2004 Ori Peleg, all rights reserved
#
# Released under the BSD license, available at:
# http://www.opensource.org/licenses/bsd-license.php
#
# Credits:
# - Dave Thomas, for commit2rss.rb: see his post and code at:
#   http://www.pragmaticautomation.com/cgi-bin/pragauto.cgi/Monitor/Loginfo2Rss.rdoc
#
# - Mark Nottingham, for module RSS.py.
#   If RSS.py wasn't included with this file, you can find it at:
#   http://www.mnot.net/python/RSS.py
#   Plus, if you're interested in creating RSS feeds, check out:
#   http://www.mnot.net/rss/tutorial/

DROP_DIR = "/path/to/drop/dir"
ITEMS_TO_KEEP = 10
CHANNEL_LINK = "" # enter link here, if you like

import sys, os, re, time, pwd
from RSS import ns, CollectionChannel

class Publisher:
    def __init__(self, filename, repositoryName):
        self.initChannel(filename, repositoryName)
        self.addItem( self._buildItemDescription() )
        self.removeExcess(ITEMS_TO_KEEP)
        self.write(filename)

    def initChannel(self, filename, repositoryName):
        try: # parse existing channel
            self.channel = CollectionChannel()
            self.channel.parse("file:" + filename)

        except: # create new channel
            title = desc = "Commit summary: %s"%repositoryName
            self.channel = self._createChannel(title, desc, CHANNEL_LINK)

    def addItem(self, description):
        title = time.strftime("%b %d, %H:%M") + " - " + self._getUser()
        self.channel.addItem( self._createItem(title, description) )

    def removeExcess(self, maxItems):
        del self.channel[(ns.rss10, "items")][maxItems:]

    def _createChannel(self, title, description, link):
        fields = { (ns.rss10, "title"):       title,
                   (ns.rss10, "description"): description,
                   (ns.rss10, "link"):        link }

        return CollectionChannel({ (ns.rss10, "channel"): fields })

    def _createItem(self, title, description):
        return { (ns.rss10, "title"):       title,
                 (ns.rss10, "description"): description,
                 (ns.dc,    "date"):        time.ctime() }

    def _buildItemDescription(self):
        def format(line):
            line = re.sub("\n$","", line) # chomp any trailing newline
            if re.match(r"[A-Z].*:\s*$", line):
                return "<p /><b>%s</b><br />" % line
            return "%s<br />" % line

        return "".join([format(line) for line in sys.stdin])

    def _getUser(self):
        try:    return pwd.getpwuid(os.getuid())[0]
        except: return "Unknown uid %s"%os.getuid()

    def write(self, filename):
        open(filename, "w").write( str(self.channel) )

# get the top-level project name
repositoryName = sys.argv[1].split("/")[0]
rssFilename = os.path.join(DROP_DIR, repositoryName+".rss")
Publisher(rssFilename, repositoryName)
