#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib, urllib2
from re import *


class Profile(object):
    """ parse profile information from a myspace.com account """

    def __init__(self, uid):
        self.uid = uid
        self.profile_url = 'http://profile.myspace.com/'
        self.fake_browser = 'Opera/8.53 (Windows NT 5.1; U; de)'
        self.site = self.__ua()


    def __ua(self):
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', self.fake_browser)]
        site = opener.open(self.profile_url+self.uid)
        site = site.read()
        if site:
            return site
        else:
            return False


    def getProfile(self):
        re = compile('<meta name="description" content="MySpace Profile - ([^"]+)" /><meta', I)
        profile_data = re.findall(self.site)
        return profile_data[0].split(', ')


p = Profile(uid="textacrew")
print p.getProfile()
