#! /usr/bin/env python
"""Compute differences and similarities between a pair of sequences.

After finding the "difflib.SequenceMatcher" class unsuitable, this module
was written and re-written several times into the polished version below."""

################################################################################

__author__ = 'Stephen "Zero" Chappell <Noctis.Skytower@gmail.com>'
__date__ = '11 February 2010'
__version__ = '$Revision: 3 $'

################################################################################

class Slice:

    __slots__ = 'prefix', 'root', 'suffix'

    def __init__(self, prefix, root, suffix):
        self.prefix = prefix
        self.root = root
        self.suffix = suffix

################################################################################

class Match:

    __slots__ = 'a', 'b', 'prefix', 'suffix', 'value'

    def __init__(self, a, b, prefix, suffix, value):
        self.a = a
        self.b = b
        self.prefix = prefix
        self.suffix = suffix
        self.value = value

################################################################################

class Tree:

    __slots__ = 'nodes', 'index', 'value'

    def __init__(self, nodes, index, value):
        self.nodes = nodes
        self.index = index
        self.value = value

################################################################################

def search(a, b):
    # Initialize startup variables.
    nodes, index = [], []
    a_size, b_size = len(a), len(b)
    # Begin to slice the sequences.
    for size in range(min(a_size, b_size), 0, -1):
        for a_addr in range(a_size - size + 1):
            # Slice "a" at address and end.
            a_term = a_addr + size
            a_root = a[a_addr:a_term]
            for b_addr in range(b_size - size + 1):
                # Slice "b" at address and end.
                b_term = b_addr + size
                b_root = b[b_addr:b_term]
                # Find out if slices are equal.
                if a_root == b_root:
                    # Create prefix tree to search.
                    a_pref, b_pref = a[:a_addr], b[:b_addr]
                    p_tree = search(a_pref, b_pref)
                    # Create suffix tree to search.
                    a_suff, b_suff = a[a_term:], b[b_term:]
                    s_tree = search(a_suff, b_suff)
                    # Make completed slice objects.
                    a_slic = Slice(a_pref, a_root, a_suff)
                    b_slic = Slice(b_pref, b_root, b_suff)
                    # Finish the match calculation.
                    value = size + p_tree.value + s_tree.value
                    match = Match(a_slic, b_slic, p_tree, s_tree, value)
                    # Append results to tree lists.
                    nodes.append(match)
                    index.append(value)
        # Return largest matches found.
        if nodes:
            return Tree(nodes, index, max(index))
    # Give caller null tree object.
    return Tree(nodes, index, 0)
