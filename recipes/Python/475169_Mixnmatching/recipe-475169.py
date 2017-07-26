#!/usr/bin/env python
# mixnmatch.py - find combination of files/dirs that sum below a given threshold
# -- Jose Fonseca

import os
import os.path
import optparse
import sys

from sets import ImmutableSet as set


def get_size(path, block_size):
    if os.path.isdir(path):
        result = 0
        for name in os.listdir(path):
            size = get_size(os.path.join(path, name), block_size)
            size = (size + block_size - 1)//block_size*block_size
            result += size
        return result
    else:
        return os.path.getsize(path)


def mix_and_match(limit, items, verbose = False):

    # filter items
    items = [(size, name) for size, name in items if size <= limit]
    # sort them by size
    items.sort(lambda (xsize, xname), (ysize, yname): cmp(xsize, ysize))
    
    # initialize variables
    added_collections = dict([(set([name]), size) for size, name in items])
    collections = added_collections

    while True:
        if verbose:
            sys.stderr.write("%d\n" % len(collections))
        
        # find unique combinations of the recent collections 
        new_collections = {}
        for names1, size1 in added_collections.iteritems():
            for size2, name2 in items:
                size3 = size1 + size2
                if size3 > limit:
                    # we can break here as all collections that follow are
                    #  bigger in size due to the sorting above
                    break
                if name2 in names1:
                    continue
                names3 = names1.union(set([name2]))
                if names3 in new_collections:
                    continue
                new_collections[names3] = size3
    
        if len(new_collections) == 0:
            break
        
        collections.update(new_collections)
        added_collections = new_collections

    return [(size, names) for names, size in collections.iteritems()]


def main():
    parser = optparse.OptionParser(usage="\n\t%prog [options] path ...")
    parser.add_option(
        '-l', '--limit', 
        type="int", dest="limit", default=4700000000, 
        help="total size limit")
    parser.add_option(
        '-B', '--block-size', 
        type="int", dest="size", default=2048, 
        help="use this block size")
    parser.add_option(
        '-s', '--show', 
        type="int", dest="show", default=10, 
        help="number of combinations to show")
    parser.add_option(
        '-v', '--verbose', 
        action="store_true", dest="verbose", default=False, 
        help="verbose output")
    (options, args) = parser.parse_args(sys.argv[1:])

    limit = options.limit
    block_size = options.size
    
    items = [(get_size(arg, block_size), arg) for arg in args]
    
    collections = mix_and_match(limit, items, options.verbose)
    collections.sort(lambda (xsize, xnames), (ysize, ynames): cmp(xsize, ysize))
    if options.show != 0:
        collections = collections[-options.show:]
    
    for size, names in collections:
        percentage = 100.0*float(size)/float(limit)
        try:
            sys.stdout.write("%10d\t%02.2f%%\t%s\n" % (size, percentage, " ".join(names)))
        except IOError:
            # ignore broken pipe
            pass 


if __name__ == '__main__':
    main()
