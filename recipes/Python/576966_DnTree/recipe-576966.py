#!/usr/bin/env python
# coding: utf-8
#
# Copyright (c) 2009 Andrew Grigorev <andrew@ei-grad.ru>
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
#

class DnTree:
    """
    Represent a set of distinguished names as tree.

    Build a hierarchy of Internet Domain names or LDAP DN.
    """

    def __init__(self, all_dn=set(), delimeter="."):
        """
        Create new DnTree object.

        all_dn    - set of dn to initially add to a tree
        delimeter - delimter used to split relative name and parent DN.
        """

        self.delimeter = delimeter

        self.childs = {}
        self.parent = {}
        self.fake_parent = {} # distinguished name of a node
                              # that should be a parent
                              # but not exists in a current tree

        self.dn_set = set() # all nodes in a tree

        self.parent[""] = ""
        self.childs[""] = [] # used by get_roots()

        for dn in all_dn:
            self.add(dn)

    def __str__(self):
        "Draw tree in ASCII graphics."

        def print_node(dn, prefix=""):
            if self.parent[dn] == "":
                ret1 = "%s%s\n" % ( prefix, dn)
            else:
                ret1 = "%s%s\n" % ( prefix, self.get_rdn(dn))
            for i in self.get_childs(dn):
                ret1 += print_node(i, prefix+" ")
            return ret1

        ret = ""
        for i in self.get_roots():
            ret += print_node(i)
        return ret

    def __repr__(self):
        return '<DnTree(%s)>' % ", ".join(self.get_roots())

    def get_roots(self):
        "Return list of root nodes without parent."
        try:
            return self.childs[""]
        except KeyError:
            return []

    def get_childs(self, dn):
        "Return list of childs of dn."
        if dn in self.childs.keys():
            return self.childs[dn]
        return []

    def get_parent_dn(self, dn):
        """Return distinguished name of parent node (if it belongs to tree,
        else return empty string).

        dn --- distinguished name of node, which parent to return
        """
        _len = dn.find(self.delimeter)
        if _len == -1:
            return ""
        else:
            if dn[_len+1:] in self.dn_set:
                return dn[_len+1:]
            else:
                return ""

    def get_fake_parent_dn(self, dn):
        """Get distinguished name of node that should be a parent of dn,
        although it does not belongs to tree.

        dn --- distinguished name of node, which fake parent to return
        """
        _len = dn.find(self.delimeter)
        if _len == -1:
            return ""
        else:
            return dn[_len+1:]

    def get_rdn(self, dn):
        """Get relative distinguished name.

        dn --- distinguished name
        """
        _len = dn.find(self.delimeter)
        if _len == -1:
            return dn
        else:
            return dn[:_len]

    def add(self, dn):
        """Add node to tree.

        dn --- distinguished name of node.
        """

        if dn in self.dn_set:
            raise ValueError('A record with dn=%s already exists!' % dn)

        parent_dn = self.get_parent_dn(dn)
        fake_parent = self.get_fake_parent_dn(dn)

        if parent_dn != fake_parent:
            try:
                self.fake_parent[fake_parent].append(dn)
            except KeyError:
                self.fake_parent[fake_parent] = [dn]

        self.parent[dn] = parent_dn
        try:
            self.childs[parent_dn].append(dn)
        except KeyError:
            self.childs[parent_dn] = [dn]

        try:
            for i in self.fake_parent.pop(dn):
                self.childs[""].remove(i)
                self.parent[i] = dn
                try:
                    self.childs[dn].append(i)
                except KeyError:
                    self.childs[dn] = [i]
        except KeyError:
            pass

        self.dn_set.add(dn)

    def rename(self, old_dn, new_dn):
        """Rename node.

        old_dn --- old distinguished name of node.
        new_dn --- new distinguished name of node.
        """
        if old_dn not in self.dn_set:
            raise ValueError("A record with dn=%s don't exists!" % new_dn)
        if new_dn in self.dn_set:
            raise ValueError("A record with dn=%s already exists!" % new_dn)
        self.remove(old_dn)
        self.add(new_dn)

    def remove(self, dn):
        """Remove node and its subtree.

        dn --- distinguished name of node.
        """

        if dn not in self.dn_set:
            raise ValueError('A record with dn=%s doesn\'t exists!' % dn)

        parent = self.get_parent_dn(dn)
        fake_parent = self.get_fake_parent_dn(dn)

        if parent != fake_parent:
            self.fake_parent[fake_parent].remove(dn)

        self.childs[parent].remove(dn)

        if dn in self.childs.keys():
            childs = tuple(self.childs[dn])
            for i in childs:
                self.remove(i)
            self.childs.pop(dn)

        self.parent.pop(dn)
        self.dn_set.remove(dn)


if __name__ == '__main__':

    import sys

    try:
        import ldap
    except ImportError:
        print('You need python-ldap installed to run this.')
        sys.exit(1)

    if len(sys.argv) not in (5, 6):
        print '''
    Using:
        python %s <uri> <bind_dn> <bind_pw> <base_dn> [<filter>]
''' % sys.argv[0]
        sys.exit(1)

    uri = sys.argv[1]
    bind_dn = sys.argv[2]
    bind_pw = sys.argv[3]
    base_dn = sys.argv[4]
    search_filter = '(objectClass=*)'

    if len(sys.argv) == 6:
        search_filter = sys.argv[5]

    conn = ldap.initialize(uri)
    conn.simple_bind_s(bind_dn, bind_pw)

    res = conn.search_s(base_dn, ldap.SCOPE_SUBTREE, search_filter, [])

    print str(DnTree(set([e[0] for e in res]), ','))

#    from itertools import permutations
#
#    s = []
#    for l in range(1, 3):
#        s += [ ".".join(i) for i in permutations('12', l) ]
#
#    print 'Initialize tree with a list:'
#    print s
#
#    t = DnTree(s)
#
#    print 'Our DnTree:'
#    print t
#
#    print 'We can add, remove and rename nodes:'
#    t.add('3.2.1')
#    print t
#
#    print 'Node would be removed with its subtree:'
#    t.remove('2.1')
#    print t # removed both '2.1' and '3.2.1'
#
#    print "And '3.2.1' is not in subtree of '1':"
#    t.add('3.2.1')
#    print t
#
#    print 'Remove 1:'
#    t.remove('1')
#    print t
