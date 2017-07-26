#! /usr/bin/env python
"""Give a string-oriented API to the generic "diff" module.

The "diff" module is very powerful but practically useless on its own.
The "search" and "empty_master" functions below resolve this problem."""

################################################################################

__author__ = 'Stephen "Zero" Chappell <Noctis.Skytower@gmail.com>'
__date__ = '11 February 2010'
__version__ = '$Revision: 3 $'

################################################################################

import diff

################################################################################

# Matching Sensitivity - OFF
CASE_AND_PUNCTUATION = False

################################################################################

def connect_tree(tree):
    """Takes the master and finds out what part of the slave matches it.

    The tree from "diff.search" may contain several different routes for
    finding matches. This function takes the best one, gets the master
    match, and fills in the prefix and suffix with the best choices."""
    match = tree.nodes[tree.index.index(tree.value)]
    node = match.a
    if match.prefix.value:
        node.prefix = connect_tree(match.prefix)
    if match.suffix.value:
        node.suffix = connect_tree(match.suffix)
    return node

def flatten_tree(node):
    """Flattens a tree from "connect_tree" for linear iteration.

    The root node created after connecting a tree must be traversed from
    beginning to end in a linear fashion. This function flattens the tree
    to make that possible. Further processing is done by other functions."""
    array = [0]
    _flatten(node, array)
    return array

def _flatten(node, array):
    """Recursively traverse and flatten the given tree.

    This is a helper function that takes "node" and sequentially processes
    its prefix, root, and suffix. The results are appended to the array."""
    if isinstance(node.prefix, diff.Slice):
        _flatten(node.prefix, array)
    else:
        array.append(node.prefix)
    array[0] += 1
    array.append((array[0], node.root))
    if isinstance(node.suffix, diff.Slice):
        _flatten(node.suffix, array)
    else:
        array.append(node.suffix)

default = lambda words: ' '.join('_' * len(word) for word in words)

################################################################################

# Note: search, build_answer, & empty_master documentation is copied!
# ------^^^^^^--^^^^^^^^^^^^----^^^^^^^^^^^^-------------------------

if CASE_AND_PUNCTUATION:

    def search(master, slave):
        """Search for differences in the master and slave strings.

        The strings are translated into key and data, and their difference
        is calculated. An answer is composed after further processing and
        returned with the number of right words and total number of words."""
        key = tuple(master.split())
        data = tuple(slave.split())
        tree = diff.search(key, data)
        if tree.value:
            node = connect_tree(tree)
            array = flatten_tree(node)
            answer = build_answer(array)
        else:
            answer = default(key)
        return tree.value, len(key), answer

    def build_answer(array):
        """Take in flattened / serialized data and generate a hint.

        This implementation returns a string useful for Verse objects.
        Incorrect or missed words get printed up as empty blank lines."""
        cache = []
        for chunk in array:
            if chunk and isinstance(chunk, tuple):
                if isinstance(chunk[0], int):
                    for word in chunk[1]:
                        cache.append(word)
                else:
                    for word in chunk:
                        cache.append('_' * len(word))
        return ' '.join(cache)

    def empty_master(master):
        """Compute the represenation of a master without a slave."""
        return default(master.split())

################################################################################

else:

    def search(master, slave):
        """Search for differences in the master and slave strings.

        The strings are translated into key and data, and their difference
        is calculated. An answer is composed after further processing and
        returned with the number of right words and total number of words."""
        words = master.split()
        key = simplify(words)
        assert len(words) == len(key), 'Cannot Simplify Words'
        data = simplify(slave.split())
        tree = diff.search(key, data)
        if tree.value:
            node = connect_tree(tree)
            array = flatten_tree(node)
            pairs = flatten_list(array)
            answer = build_answer(words, pairs)
        else:
            answer = default(key)
        return tree.value, len(key), answer

    def simplify(words):
        """Remove non-alphabetic characters from an array of words."""
        letter = lambda s: ''.join(filter(lambda s: 'a' <= s <= 'z', s))
        return tuple(filter(bool, map(letter, map(str.lower, words))))

    def flatten_list(array):
        """Build (flag, load) pairs for the "build_answer" function."""
        pairs = []
        for chunk in array:
            if chunk and isinstance(chunk, tuple):
                if isinstance(chunk[0], int):
                    for word in chunk[1]:
                        pairs.append((True, word))
                else:
                    for word in chunk:
                        pairs.append((False, word))
        return pairs

    def build_answer(words, pairs):
        """Take in flattened / serialized data and generate a hint.

        This implementation returns a string useful for Verse objects.
        Incorrect or missed words get tranformed into underscore lines."""
        cache = []
        for word, (flag, load) in zip(words, pairs):
            cache.append(word if flag else '_' * len(load))
        return ' '.join(cache)

    def empty_master(master):
        """Compute the represenation of a master without a slave."""
        return default(simplify(master.split()))
