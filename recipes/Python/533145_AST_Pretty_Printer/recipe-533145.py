"""Python AST pretty-printer.

To me, it is totally unf*ckinbelievable that the standard Python compiler module
does not come with a pretty-printer for the AST. Here is one.
"""

import sys
from compiler.ast import Node


def pprintAst(ast, indent='  ', stream=sys.stdout):
    "Pretty-print an AST to the given output stream."
    rec_node(ast, 0, indent, stream.write)

def rec_node(node, level, indent, write):
    "Recurse through a node, pretty-printing it."
    pfx = indent * level
    if isinstance(node, Node):
        write(pfx)
        write(node.__class__.__name__)
        write('(')

        if any(isinstance(child, Node) for child in node.getChildren()):
            for i, child in enumerate(node.getChildren()):
                if i != 0:
                    write(',')
                write('\n')
                rec_node(child, level+1, indent, write)
            write('\n')
            write(pfx)
        else:
            # None of the children as nodes, simply join their repr on a single
            # line.
            write(', '.join(repr(child) for child in node.getChildren()))

        write(')')

    else:
        write(pfx)
        write(repr(node))


if __name__ == '__main__':
    def test():
        import compiler
        pprintAst(compiler.parseFile(__file__))
    test()
