# -*- coding: utf-8 -*-

# Copyright (c) 2015 Zachary Weinberg
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""Extract compilation commands from Distutils for use in a makefile.
Here is an example makefile that builds two modules, mod1 and mod2,
using this program:

    CC     = cc
    CXX    = c++
    PYTHON = python

    all: # is the default.
    include python-vars.mk

    all: mod1.$M mod2.$M

    # mod1 is written in C; mod2 is written in C++
    mod1.$M: LIBS = -lthis -lthat
    mod1.$M: foo.$O bar.$O baz.$O
            $(CC) $(LINKER_ARGS)

    mod2.$M: quux.$O blurf.$O
            $(CXX) $(LINKER_ARGS)

    # Header-file dependencies
    foo.$O: foo.h bar.h
    bar.$O: bar.h baz.h
    baz.$O: baz.h
    quux.$O: quux.h blurf.h
    blurf.$O: blurf.h

    clean:
            -rm -f mod1.$M mod2.$M foo.$O bar.$O baz.$O quux.$O blurf.$O

    # Boilerplate; you shouldn't need to change anything below.
    python-vars.mk:
            $(PYTHON) get-module-compile-cmds.py $@

    %.$O: %.c
        $(CC) $(COMPILER_ARGS)
    %.$O: %.cc
        $(CXX) $(COMPILER_ARGS)

    .PHONY: all clean

The sample code shown above assumes GNU Make, but the output of this
program should be usable with any make implementation that supports
$<, $^, and $@.

Installation is not currently supported.
"""

from distutils.dist import Distribution
from distutils.command.build_ext import build_ext
from distutils.log import set_verbosity

# io.StringIO exists in 2.7 but doesn't play nice with distutils, so
# try the old cStringIO first.
try:
    from cStringIO import StringIO
except:
    from io import StringIO

# shlex.quote is the documented API for shell quotation, but only
# exists in 3.3 and later. pipes.quote is undocumented but has existed
# since 2.0.
import shlex
try:
    from shlex import quote as shellquote
except:
    from pipes import quote as shellquote

import sys

if len(sys.argv) != 2:
    raise SystemExit("usage: $(PYTHON) {} output-file"
                     .format(sys.argv[0]))

# There is no way to get distutils to just _tell_ you what commands
# are; you have to run them, in dry-run mode so it doesn't actually do
# anything, and capture the echoed command lines.
class CaptureStdout:
    def __init__(self):
        self.old_stdout = None
        self.stdout = StringIO()

    def __enter__(self):
        self.old_stdout = sys.stdout
        sys.stdout = self.stdout
        return self.stdout

    def __exit__(self, *dontcare):
        sys.stdout = self.old_stdout
        self.stdout.close()

# What one gets back from the captured stdout needs a little
# postprocessing in order to be usable in a Makefile.
def munge_command(inputvar, srcext, objextname, cmd):
    cmd = shlex.split(cmd.strip())
    munged = []
    # The first thing on the line will be the compiler itself; throw
    # that out.  Find dummy.srcext and dummy.objext, and substitute
    # appropriate Makefile variable names. Also, determine what objext
    # actually is.
    dummy_srcext = "dummy." + srcext
    objext = None
    for arg in cmd[1:]:
        if arg == dummy_srcext:
            munged.append(inputvar) # either $< or $^, depending
        elif arg.startswith("dummy."):
            munged.append("$@")
            objext = arg[len("dummy."):]
        else:
            if shellquote(arg) != arg:
                raise SystemExit("error: command {!r}: "
                                 "cannot put {!r} into a makefile"
                                 .format(cmd, arg))
            munged.append(arg)

    if not objext:
        raise SystemExit("error: command {!r}: failed to determine {}"
                         .format(cmd, objextname))

    return " ".join(munged), objext

# The easiest way to ensure that we use a properly configured compiler
# is to subclass build_ext, because some of the work for that is only
# done when build_ext.run() is called, grumble.
class stub_build_ext_report:
    def __init__(self):
        self.compile_command = None
        self.link_command = None
        self.objext = None
        self.modext = None

class stub_build_ext(build_ext):
    def __init__(self, reporter, *args, **kwargs):
        self.reporter = reporter
        build_ext.__init__(self, *args, **kwargs)

    def build_extensions(self):
        with CaptureStdout() as cap:
            self.compiler.compile(["dummy.c"], output_dir="")
            ccmd = cap.getvalue()

        ccmd, objext = munge_command("$<", "c", "objext", ccmd)
        self.reporter.compile_command = ccmd
        self.reporter.objext = objext

        with CaptureStdout() as cap:
            self.compiler.link_shared_object(
                ["dummy." + objext],
                self.get_ext_filename("dummy"))
            lcmd = cap.getvalue()

        lcmd, modext = munge_command("$^ $(LIBS)", objext, "modext",
                                     lcmd)
        self.reporter.link_command = lcmd
        self.reporter.modext = modext

# The generated Makefile fragment should depend on the physical file for
# every Distutils module that has been loaded by this program.
def get_fragment_dependencies():
    distutils_modules = sorted(m.__file__ for n, m in sys.modules.items()
                               if n.startswith("distutils"))
    return " \\\n\t".join(distutils_modules)

results   = stub_build_ext_report()

set_verbosity(1)
fake_dist = Distribution({"ext_modules": "not empty"})
fake_build_ext = stub_build_ext(results, fake_dist)
fake_build_ext.inplace = True
fake_build_ext.dry_run = True
fake_build_ext.finalize_options()
fake_build_ext.run()

# Sanity check.
if (not results.objext or
    not results.modext or
    not results.compile_command or
    not results.link_command):
    raise SystemExit("failed to probe compilation environment")

with open(sys.argv[1], "w") as f:
    f.write("""\
O             = {objext}
M             = {modext}
COMPILER_ARGS = {compile}
LINKER_ARGS   = {link}
""".format(objext  = results.objext,
           modext  = results.modext,
           compile = results.compile_command,
           link    = results.link_command))

    f.write("\n{}: {} \\\n\t{}\n"
            .format(sys.argv[1], sys.argv[0],
                    get_fragment_dependencies()))
