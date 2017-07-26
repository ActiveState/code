from __future__ import generators # needed for Python 2.2
import sys

def walktree(top = ".", depthfirst = True):
    """Walk the directory tree, starting from top. Credit to Noah Spurrier and Doug Fort."""
    import os, stat, types
    names = os.listdir(top)
    if not depthfirst:
        yield top, names
    for name in names:
        try:
            st = os.lstat(os.path.join(top, name))
        except os.error:
            continue
        if stat.S_ISDIR(st.st_mode):
            for (newtop, children) in walktree (os.path.join(top, name), depthfirst):
                yield newtop, children
    if depthfirst:
        yield top, names

def makeHTMLtable(top, depthfirst=False):
    from xml.sax.saxutils import escape # To quote out things like &amp;
    ret = ['<table class="fileList">\n']
    for top, names in walktree(top):
        ret.append('   <tr><td class="directory">%s</td></tr>\n'%escape(top))
        for name in names:
            ret.append('   <tr><td class="file">%s</td></tr>\n'%escape(name))
    ret.append('</table>')
    return ''.join(ret) # Much faster than += method

def makeHTMLpage(top, depthfirst=False):
    return '\n'.join(['<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"',
                      '"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">',
                      '<html>'
                      '<head>',
                      '   <title>Search results</title>',
                      '   <style type="text/css">',
                      '      table.fileList { text-align: left; }',
                      '      td.directory { font-weight: bold; }',
                      '      td.file { padding-left: 4em; }',
                      '   </style>',
                      '</head>',
                      '<body>',
                      '<h1>Search Results</h1>',
                      makeHTMLtable(top, depthfirst),
                      '</body>',
                      '</html>'])
                   
if __name__ == '__main__':
    if len(sys.argv) == 2:
        top = sys.argv[1]
    else: top = '.'
    print makeHTMLpage(top)
