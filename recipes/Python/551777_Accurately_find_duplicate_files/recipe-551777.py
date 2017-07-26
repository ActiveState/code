#!/usr/bin/env python
#
# find-duplicates
# by Keith Gaughan <http://talideon.com/>
#
# Finds an lists any duplicate files in the given directories.
#
# Copyright (c) Keith Gaughan, 2008.
# All Rights Reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#  1. Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.
#
#  2. Redistributions in binary form must reproduce the above copyright
#     notice, this list of conditions and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY AUTHOR AND CONTRIBUTORS "AS IS" AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL AUTHOR OR CONTRIBUTORS BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
# THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# This license is subject to the laws and courts of the Republic of Ireland.
#

from __future__ import with_statement
import sys
import os
import hashlib
import getopt
import filecmp


USAGE = "Usage: %s [-h] [-m<crc|md5>] <dir>*"


class crc:
    """
    Wraps up zlib.crc32 to make it suitable for use as a faster but less
    accurate alternative to the hashlib.* classes.
    """
    def __init__(self, initial=None):
        self.crc = 0
        if initial is not None:
            self.update(initial)
    def update(self, block):
        import zlib
        self.crc = zlib.crc32(block, self.crc)
    def hexdigest(self):
        return "%X" % self.crc
    def digest(self):
        # Er...
        return self.crc


def all_files(*tops):
    """Lists all files in the given directories."""
    for top in tops:
        for dirname, _, filenames in os.walk(top):
            for f in filenames:
                path = os.path.join(dirname, f)
                if os.path.isfile(path):
                    yield path


def digest(file, method=hashlib.md5):
    with open(file) as f:
        h = method(f.read()).digest()
    return h


def true_duplicates(files):
    """
    Compare the given files, breaking them down into groups with identical
    content.
    """
    while len(files) > 1:
        next_set = []
        this_set = []
        master = files[0]
        this_set.append(master)
        for other in files[1:]:
            if filecmp.cmp(master, other, False):
                this_set.append(other)
            else:
                next_set.append(other)
        if len(this_set) > 1:
            yield this_set
        files = next_set


def group_by(groups, grouper, min_size=1):
    """Breaks each of the groups into smaller subgroups."""
    for group in groups:
        subgroups = {}
        for item in group:
            g = grouper(item)
            if not subgroups.has_key(g):
                subgroups[g] = []
            subgroups[g].append(item)
        for g in subgroups.itervalues():
            if len(g) >= min_size:
                yield g


def usage(message=None):
    global USAGE
    fh = sys.stdout
    exit_code = 0
    if message:
        fh = sys.stderr
        exit_code = 2
        print >>fh, str(message)
    name = os.path.basename(sys.argv[0])
    print >>fh, USAGE % (name,)
    sys.exit(exit_code)


def main():
    try:
        opts, paths = getopt.getopt(sys.argv[1:], "hm:")
    except getopt.GetoptError, err:
        usage(err)
    method = crc
    for o, a in opts:
        if o == "-m":
            if a == "crc":
                method = crc
            elif a == "md5":
                method = hashlib.md5
            else:
                usage("Unknown grouping method: %s" % (a,))
        elif o == "-h":
            usage()
        else:
            usage("Unknown option: %s%s" % (o, a))

    if len(paths) == 0:
        paths = ["."]

    first = True
    groups = [all_files(*paths)]
    for grouper in [os.path.getsize, lambda file: digest(file, method)]:
        groups = group_by(groups, grouper, 2)
    for group in groups:
        for files in sorted(true_duplicates(group)):
            if first:
                first = False
            else:
                print
            for file in files:
                print file


if __name__ == "__main__":
    main()
