# -*- coding: utf-8 -*-
from re import compile as compile_regex

_MULTIPLE_PATHS = compile_regex(r"/{2,}")


def normalize_path(path):
    """
    Normalize ``path``.
    
    It returns ``path`` with leading and trailing slashes, and no multiple
    continuous slashes.
    
    """
    if path:
        if path[0] != "/":
            path = "/" + path
        
        if path[-1] != "/":
            path = path + "/"
        
        path = _MULTIPLE_PATHS.sub("/", path)
    else:
        path = "/"
    
    return path


# ------ UNIT TESTS ------
from nose.tools import eq_


class TestNormalizingPath(object):
    """Tests for :func:`normalize_path`."""
    
    def test_empty_string(self):
        path_normalized = normalize_path("")
        eq_(path_normalized, "/")
    
    def test_slash(self):
        path_normalized = normalize_path("/")
        eq_(path_normalized, "/")
    
    def test_no_leading_slash(self):
        path_normalized = normalize_path("path/")
        eq_(path_normalized, "/path/")
    
    def test_no_trailing_slash(self):
        path_normalized = normalize_path("/path")
        eq_(path_normalized, "/path/")
    
    def test_trailing_and_leading_slashes(self):
        path_normalized = normalize_path("/path/")
        eq_(path_normalized, "/path/")
    
    def test_multiple_leading_slashes(self):
        path_normalized = normalize_path("////path/")
        eq_(path_normalized, "/path/")
    
    def test_multiple_trailing_slashes(self):
        path_normalized = normalize_path("/path////")
        eq_(path_normalized, "/path/")
    
    def test_multiple_inner_slashes(self):
        path_normalized = normalize_path("/path////here/")
        eq_(path_normalized, "/path/here/")
    
    def test_unicode_path(self):
        path_normalized = normalize_path(u"mañana/aquí")
        eq_(path_normalized, u"/mañana/aquí/")
