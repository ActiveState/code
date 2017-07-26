#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       cherrytarball.py
#
#       Copyright 2009 Dan McDougall <YouKnowWho@YouKnowWhat.com>
#
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; Version 3 of the License
#
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, the license can be downloaded here:
#
#       http://www.gnu.org/licenses/gpl.html

"""
CherryTarball.py
    An example of how to serve up static content from inside of a gzipped tarball
"""
import os
import tarfile
import cherrypy

# The location of the gzipped tarball containing your static content
tarball_path = '/var/www/static.tar.gz'

class CherryTarball(object):
    def index(self):
        """Return an HTML page using static()."""

        # 'html/index.html' is the path WITHIN the tarball.
        return self.static('html/index.html')

    def static(self, filepath):
        """Returns static content from within our gzip-compressed tar file.

        For this example, here's the theoretical layout of static.tar.gz:
        $ tar -ztvf static.tar.gz
        drwxr-xr-x user/staff     0 2008-12-22 22:48 html/
        -rw-r--r-- user/staff  1922 2008-12-22 22:43 html/index.html
        -rw-r--r-- user/staff   200 2008-12-22 22:43 css/default.css
        drwxr-xr-x user/staff     0 2008-12-22 22:48 images/
        -rw-r--r-- user/staff  1432 2008-12-22 22:43 images/logo.gif
        ...and index.html loads both css/default.css and images/logo.gif
        """
        tar = tarfile.open(tarball_path)
        fileobj = tar.extractfile(filepath)
        f, extension = os.path.splitext(filepath)
        if extension == '.css': # It seems CherryPy can't always figure out what mime types are inside tarballs
            cherrypy.response.headers['Content-Type'] = "text/css"
        filedata = fileobj.read()
        return filedata

def setup_routes():
    """Setup dispatcher routes (i.e. URL paths)"""
    root = CherryTarball()
    d = cherrypy.dispatch.RoutesDispatcher()
    d.connect('main', '/', controller=root)
    # This enumerates the tarball and connects each file within to a URL in the dispatcher
    tar = tarfile.open(tarball_path)
    for tarobj in tar.getmembers():
        if tarobj.isdir():
            pass # Skip directories
        else:
            d.connect(tarobj.name, tarobj.name, controller=root, action='static', filepath=tarobj.name)
    dispatcher = d
    return dispatcher

if __name__ == "__main__":
    conf = {
        '/': {
            'request.dispatch': setup_routes(),
        },
    }
    app = cherrypy.tree.mount(None, config=conf)
    cherrypy.quickstart(app)
