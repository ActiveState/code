#!/usr/bin/env python

# AST Visitor generator recipe
#
# Lonnie Princehouse, 2004

import re

# Set this to the current location of the compiler ast module HTML doc
# (the page that has a table of AST Node types and attributes)
compiler_ast_doc_url = 'http://docs.python.org/lib/module-compiler.ast.html'

klass = '<tt class="class">(?P<klass>\S+?)</tt></td>'
member = '<td><tt class="member">(?P<member>\S+)</tt></td>\s+<td>(?P<doc>.*?)</td>'
finder = re.compile("%s|%s" % (klass, member))

nodes = []

class ASTDocNode:
    def __init__(self, name):
        self.name = name
        self.attributes = []
    def add_attribute(self, attribute, comment):
        self.attributes.append( (attribute, comment) )
    def __str__(self):
        atlist = []
        for a,c in self.attributes:
            if a:
                if c == '&nbsp;':
                    c = ''
                atlist.append("        #     %-16s %s" % (a,c))
        attribute_list = '\n'.join(atlist)
        name = self.name
        return """
    def visit%(name)s(self, node):
        # %(name)s attributes
%(attribute_list)s
        raise NotImplementedException('visit%(name)s')""" % locals()

def generate_visitor_skeleton(output_stream, url = compiler_ast_doc_url, node_class = ASTDocNode, visitor_class_name = 'VisitorSkeleton'):
    import urllib
    document = urllib.urlopen(url)
    html_source = document.read()
    document.close()
    header = """

import compiler.visitor

class NotImplementedException(Exception): pass

class %s(compiler.visitor.ASTVisitor): """ % visitor_class_name

    for klass, attribute, comment in finder.findall(html_source):
        if klass not in ('', '&nbsp;'):
            nodes.append(node_class(klass))
        else:
            nodes[-1].add_attribute(attribute, comment)
    
    print >> output_stream, header

    for n in nodes:
        print >> output_stream,  str(n)

if __name__ == '__main__':
    import sys
    # Optional command line argument is the URL of the Node doc.
    # This argument might be useful if (a) you don't have network access, but have a local copy of the docs.
    # or (b) you want to build a visitor for an old version of Python (at the time of this writing, current
    # docs are for 2.3.4)

    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = compiler_ast_doc_url

    generate_visitor_skeleton(sys.stdout, url)
