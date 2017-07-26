# -*- coding: iso-8859-1 -*-
#
# Code coverage colorization:
#  - sébastien Martini <sebastien.martini@gmail.com>
#    * 5/24/2006 fixed: bug when code is completely covered (Kenneth Lind).
#
# Original recipe:
#  http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/52298
#
# Original Authors:
#  - Jürgen Hermann
#  - Mike Brown <http://skew.org/~mike/>
#  - Christopher Arndt <http://chrisarndt.de>
#
import cgi
import string
import sys
import cStringIO
import os
import keyword
import token
import tokenize

_VERBOSE = False

_KEYWORD = token.NT_OFFSET + 1
_TEXT    = token.NT_OFFSET + 2

_css_classes = {
    token.NUMBER:       'number',
    token.OP:           'operator',
    token.STRING:       'string',
    tokenize.COMMENT:   'comment',
    token.NAME:         'name',
    token.ERRORTOKEN:   'error',
    _KEYWORD:           'keyword',
    _TEXT:              'text',
}

_HTML_HEADER = """\
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
  "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<title>code coverage of %(title)s</title>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">

<style type="text/css">
pre.code {
    font-style: Lucida,"Courier New";
}
.number {
    color: #0080C0;
}
.operator {
    color: #000000;
}
.string {
    color: #008000;
}
.comment {
    color: #808080;
}
.name {
    color: #000000;
}
.error {
    color: #FF8080;
    border: solid 1.5pt #FF0000;
}
.keyword {
    color: #0000FF;
    font-weight: bold;
}
.text {
    color: #000000;
}
.notcovered {
    background-color: #FFB2B2;
}
</style>

</head>
<body>
"""

_HTML_FOOTER = """\
</body>
</html>
"""

class Parser:
    """ Send colored python source.
    """
    def __init__(self, raw, out=sys.stdout, not_covered=[]):
        """ Store the source text.
        """
        self.raw = string.strip(string.expandtabs(raw))
        self.out = out
        self.not_covered = not_covered  # not covered list of lines
        self.cover_flag = False  # is there a <span> tag opened?

    def format(self):
        """ Parse and send the colored source.
        """
        # store line offsets in self.lines
        self.lines = [0, 0]
        pos = 0
        while 1:
            pos = string.find(self.raw, '\n', pos) + 1
            if not pos: break
            self.lines.append(pos)
        self.lines.append(len(self.raw))

        # parse the source and write it
        self.pos = 0
        text = cStringIO.StringIO(self.raw)
        self.out.write('<pre class="code">\n')
        try:
            tokenize.tokenize(text.readline, self)
        except tokenize.TokenError, ex:
            msg = ex[0]
            line = ex[1][0]
            self.out.write("<h3>ERROR: %s</h3>%s\n" % (
                msg, self.raw[self.lines[line]:]))
        if self.cover_flag:
            self.out.write('</span>')
            self.cover_flag = False
        self.out.write('\n</pre>')

    def __call__(self, toktype, toktext, (srow,scol), (erow,ecol), line):
        """ Token handler.
        """
        if _VERBOSE:
            print "type", toktype, token.tok_name[toktype], "text", toktext,
            print "start", srow,scol, "end", erow,ecol, "<br>"

        # calculate new positions
        oldpos = self.pos
        newpos = self.lines[srow] + scol
        self.pos = newpos + len(toktext)

        if not self.cover_flag and srow in self.not_covered:
            self.out.write('<span class="notcovered">')
            self.cover_flag = True

        # handle newlines
        if toktype in [token.NEWLINE, tokenize.NL]:
            if self.cover_flag:
                self.out.write('</span>')
                self.cover_flag = False

        # send the original whitespace, if needed
        if newpos > oldpos:
            self.out.write(self.raw[oldpos:newpos])

        # skip indenting tokens
        if toktype in [token.INDENT, token.DEDENT]:
            self.pos = newpos
            return

        # map token type to a color group
        if token.LPAR <= toktype and toktype <= token.OP:
            toktype = token.OP
        elif toktype == token.NAME and keyword.iskeyword(toktext):
            toktype = _KEYWORD
        css_class = _css_classes.get(toktype, 'text')

        # send text
        self.out.write('<span class="%s">' % (css_class,))
        self.out.write(cgi.escape(toktext))
        self.out.write('</span>')


class MissingList(list):
    def __init__(self, i):
        list.__init__(self, i)

    def __contains__(self, elem):
        for i in list.__iter__(self):
            v_ = m_ = s_ = None
            try:
                v_ = int(i)
            except ValueError:
                m_, s_ = i.split('-')
            if v_ is not None and v_ == elem:
                return True
            elif (m_ is not None) and (s_ is not None) and \
                     (int(m_) <= elem) and (elem <= int(s_)):
                return True
        return False


def colorize_file(filename, outstream=sys.stdout, not_covered=[]):
    """
    Convert a python source file into colorized HTML.

    Reads file and writes to outstream (default sys.stdout).
    """
    fo = file(filename, 'rb')
    try:
        source = fo.read()
    finally:
        fo.close()
    outstream.write(_HTML_HEADER % {'title': os.path.basename(filename)})
    Parser(source, out=outstream,
           not_covered=MissingList((not_covered and \
                                    not_covered.split(', ')) or \
                                   [])).format()
    outstream.write(_HTML_FOOTER)
