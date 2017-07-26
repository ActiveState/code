#!/usr/bin/env python

import urllib
import urlparse
import os
import re
import logging

_sub = re.compile("([^\\-/a-zA-Z0-9\\.])").sub
def _sc(ch):
    return "_%02x" % ord(ch.group(1))

def normalize_path(path, sub=_sub, sc=_sc):
    if "." not in path:
        path += "/"
    if path.endswith("/"):
        path += "index.html"
    if path and path[0] == "/":
        path = path[1:]
    path = sub(sc, path)
    return path

def localize_path(url):
    splitd = urlparse.urlsplit(url)
    if splitd[3]:
        return "%s?%s" % splitd[2:4]
    else:
        return splitd[2]

def exists_relative(url):
    path = localize_path(url)
    path = normalize_path(path)
    return os.path.exists(path)

def fetch_relative(url, proxies=None, postfetch=None):
    """postfetch is a callback that receives fetched data (as string)"""
    path = localize_path(url)
    path = normalize_path(path)
    if os.path.exists(path):
        if postfetch:
            logging.debug("reprocessing file %s" % path)
            f = open(path, "rb")
            data = f.read()
            f.close()
            postfetch(data)
        return False
    logging.debug("fetching %s" % url)
    f = urllib.urlopen(url, proxies=proxies)
    data = f.read()
    f.close()
    head, tail = os.path.split(path)
    if not os.path.exists(head):
        os.makedirs(head)
    f = open(path, "wb")
    f.write(data)
    f.close()
    if postfetch:
        postfetch(data)
    return True
