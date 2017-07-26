#!/usr/bin/env python

# Copyright (c) 2008 Florian Mayer

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

""" A simple dependency resolver """


def no_deps(items, deps, built):
    """ Get items that have no unbuilt dependencies """
    return [i for i in items if not depends_on_unbuilt(i, deps, built)]


def depends_on_unbuilt(item, deps, built):
    """ See if item depends on any item not built """
    if not item in deps:
        return False
    
    return any(d not in built for d in deps[item])


def resolve_paralell(items, deps):
    """ Returns a list of sets of tasks that can be done paralelly """
    items = set(items)
    built = set()
    out = []
    while True:
        if not items:
            break

        no_d = set(no_deps(items, deps, built))
        items -= no_d
        
        built |= no_d
        out.append(no_d)
        
        if set(sum(deps.values(), [])) == built:
            out.append(items)
            break
        
    return out


if __name__ == '__main__':
    jobs = ['a', 'b', 'c', 'd', 'e']
    deps = {'a': ['b', 'c'], 'b': ['d', 'e']}
    
    print resolve_paralell(jobs, deps)
