###Serve static web content from within a gzipped tarball to save space using CherryPy

Originally published: 2009-03-31 18:24:06
Last updated: 2009-03-31 18:24:06
Author: Dan McDougall

This code lets you store all of your static website content inside a gzipped tarball while transparently serving it to HTTP clients on-demand.  Perfect for embedded systems where space is limited.