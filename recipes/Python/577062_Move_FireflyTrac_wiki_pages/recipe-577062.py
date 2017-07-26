#!/usr/bin/env python

import xmlrpclib

# replace the usernames, passwords, and project URLs with real ones

project1 = xmlrpclib.ServerProxy("http://username:password@firefly.activestate.com/username/project1/login/xmlrpc")
project2 = xmlrpclib.ServerProxy("http://username:password@firefly.activestate.com/username/project2/login/xmlrpc")

# wiki.putPage() throw errors and quits when it tries to overwrite an
# existing wiki page. Uncomment this section to delete all pages in
# project2 first

#pagenames_project2 = project2.wiki.getAllPages()
#for name in pagenames_project2:
#    project2.wiki.deletePage(name)

pagenames_project1 = project1.wiki.getAllPages()
for name in pagenames_project1:
    page_contents = project1.wiki.getPage(name)
    project2.wiki.putPage(name, page_contents, {"comment": "Copying wiki pages"})
