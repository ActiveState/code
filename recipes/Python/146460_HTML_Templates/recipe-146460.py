# -*- mode: python; indent-tabs-mode: nil; tab-width: 4 -*-
# vim: set tabstop=4 shiftwidth=4 expandtab:

"""$Id: opagcgilib.py,v 1.1 2002/05/31 04:57:44 msoulier Exp $
This file is a common library for all CGI scripts on the OPAG site. It
contains functions necessary for parsing the site template.
"""

import re, types, os

TRUE = 1
FALSE = 0

# The replacement dictionary for parsing the template.
replacement_dict = {}
# The site template.
site_template = 'template.html'

class Replacer:
    """This class is a utility class used to provide a bound method to the
    re.sub() function."""
    def __init__(self, dict):
        """The constructor. It's only duty is to populate itself with the
        replacement dictionary passed."""
        self.dict = dict

    def replace(self, matchobj):
        """The replacement method. This is passed a match object by re.sub(),
        which it uses to index the replacement dictionary and find the
        replacement string."""
        key = matchobj.group(1)
        if self.dict.has_key(key):
            return self.dict[key]
        else:
            return ''

class OpagCGI:
    """This class represents a running instance of a CGI on the OPAG website.
    It provides methods to give output from a CGI to a user's browser while
    maintaining the site's look and feel. It does this via template parsing of
    a standard template, permitting parsing of other templates as well."""

    def __init__(self, template=site_template):
        """OpagCGI(template) -> OpagCGI object
        The class constructor, taking the path to the template to use, using
        the site template as default.
        """
        self.template = template
        self.template_file = None
        if not os.path.exists(self.template):
            raise OpagMissingPrecondition, "%s does not exist" % self.template

    def parse(self, dict, header=TRUE):
        """parse(dict) -> string
        This method parses the open file object passed, replacing any keys
        found using the replacement dictionary passed."""
        if type(dict) != types.DictType:
            raise TypeError, "Second argument must be a dictionary"
        if not self.template:
            raise OpagMissingPrecondition, "template path is not set"
        # Open the file if its not already open. If it is, seek to the
        # beginning of the file.
        if not self.template_file:
            self.template_file = open(self.template, "r")
        else:
            self.template_file.seek(0)
        # Instantiate a new bound method to do the replacement.
        replacer = Replacer(dict).replace
        # Read in the entire template into memory. I guess we'd better keep
        # the templates a reasonable size if we're going to keep doing this.
        buffer = self.template_file.read()
        replaced = ""
        if header:
            replaced = "Content-Type: text/html\n\n"
        replaced = replaced + re.sub("%%(\w+)%%", replacer, buffer)
        return replaced

class OpagRuntimeError(RuntimeError):
    """The purpose of this class is to act as the base class for all runtime
    errors in OPAG CGI code. More specific Exceptions should subclass this if
    they happen at runtime. We might want to get more specific than this in
    the future, and introduce subclasses for IO errors, type errors and such,
    but this will do for now."""

class OpagMissingPrecondition(OpagRuntimeError):
    """The purpose of this class is to represent all problems with missing
    preconditions in OPAG code, such as a file that is supposed to exist, but
    does not."""


# Copyright (C) Ottawa Python Author's Group
# Example of use:
cgi = OpagCGI()
rdict = {'email': 'msoulier@storm.ca'}
print cgi.parse(rdict)
