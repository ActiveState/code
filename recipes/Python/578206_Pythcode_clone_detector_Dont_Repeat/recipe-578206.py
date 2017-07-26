"""
Python code clone detector,
using Abstract Syntax Trees.
"""

import ast
import collections

__author__  = 'FBV'
__license__ = 'MIT'
__version__ = '0.0.2'
__status__  = 'alpha'

class Position(ast.NodeVisitor):
    '''
    Find a clone position in the code (its line-span).
    Count child nodes.
    '''
    def init(self, clone):
        '''
        Lazy initialization.
        '''
        self.begin_line = self.end_line = clone.node.lineno
        self.node_count = 0
        self.generic_visit(clone.node)
    def visit(self, node):
        '''
        Find node's line and column span.
        '''
        if hasattr(node, 'lineno'):
            self.begin_line = min(self.begin_line, node.lineno)
            self.end_line = max(self.end_line, node.lineno)
            self.node_count += 1
            self.generic_visit(node)

class Clone(collections.namedtuple('Clone', 'node file position')):
    '''
    A set of code.
    '''
    def source(self, indent=''):
        '''
        Retrieve original source code.
        '''
        if not hasattr(self.position, 'begin_line'):
            self.position.init(self)
        lines = self.file.source[
            self.position.begin_line-1:self.position.end_line]
        return (self.position.begin_line, self.position.end_line,
                '\n'.join(indent + line.rstrip() for line in lines))

class Clones(list):
    '''
    A list of identical code snippets.
    '''
    def score(self):
        '''
        Provide a score for ordering clones while reporting.
        This sorts by number of nodes in the subtree, number
        of clones of the node, and code size.
        '''
        candidate = self[0] # Pick the first clone.
        size = len(candidate.source()[-1])
        return (candidate.position.node_count, len(self), size)

class File:
    '''
    A source file.
    '''
    def __init__(self, name, source):
        '''
        Create a file with name and source-code.
        '''
        self.name = name
        self.source = source
            
def digest(node):
    '''
    Return an unambiguous string representation of a sub-tree in node.
    Emulates ast.dump(node, False).
    '''
    if isinstance(node, ast.AST):
        if not hasattr(node, '_cached'):
            node._cached = '%s(%s)' % (node.__class__.__name__, ', '.join(
                digest(b) for a, b in ast.iter_fields(node)))
        return node._cached
    elif isinstance(node, list):
        return '[%s]' % ', '.join(digest(x) for x in node)
    return repr(node)

class Index(ast.NodeVisitor):
    '''
    A source code repository.
    '''
    def __init__(self, exclude):
        '''
        Create a new file indexer.
        '''
        self.nodes = collections.defaultdict(Clones)
        self.blacklist = frozenset(exclude)
    def add(self, file):
        '''
        Add a file to the index and parse it.
        '''
        source = open(file).readlines()
        tree = ast.parse(''.join(source))
        self._file = File(file, source)
        self.generic_visit(tree)
    def visit(self, node):
        '''
        Walk the Abstract Syntax Tree of a file.
        Convert each sub-tree to a string, which is used 
        as a key in the clones dictionnary.
        '''
        if hasattr(node, 'lineno'):
            if node.__class__.__name__ not in self.blacklist:
                expr = digest(node)
                self.nodes[expr].append(
                    Clone(node, self._file, Position()))
        self.generic_visit(node)
    def clones(self):
        '''
        Returns a list of duplicate constructs.
        '''
        return sorted(((expr, nodes) 
            for expr, nodes in self.nodes.items() if len(nodes)>1),
                key=lambda n: n[1].score(), reverse=True)        

if __name__ == '__main__':
    import argparse
    import itertools

    # Parse command-line arguments.
    args = argparse.ArgumentParser(description=__doc__)
    args.add_argument('files', 
        metavar='FILE', nargs='+', 
        help='set of Python files to check for duplicate code')
    args.add_argument('--ignore', '-i',
        metavar='NODE', nargs='+', default=['Name'], 
        help='skip some syntactic constructs (default: Name)')
    args.add_argument('--min', '-m',
        metavar='N', type=int, default=0, 
        help='report items duplicated at least N times')
    args.add_argument('--version', '-v', 
        action='version', version='%(prog)s ' + __version__)
    input = args.parse_args()

    # Process files.
    sources = Index(input.ignore)    
    for file in input.files:
        sources.add(file)

    # Report clones.
    for expr, clones in sources.clones():
        if len(clones) >= input.min:
            print("+%d repetitions of: %s ->" % 
                    (len(clones), expr))
            for file, group in itertools.groupby(clones, 
                    lambda clone: clone.file.name):
                print("  - in %s" % file)
                for clone in group:
                    begin, end, source = clone.source(' '*8)
                    if begin == end:
                        line = 'line %d' % begin
                    else:
                        line = 'lines %d to %d' % (begin, end)
                    print('      %s:\n%s' % (line, source))
