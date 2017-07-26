from itertools import islice, repeat, izip, cycle

# If PEP 3102 is accepted, the signature would be
#def iterCombinations(*iterables, blocksize=1):
def iterCombinations(*iterables, **kwds):
    '''Generates the combinations of the given iterables.
    
    @returns: An iterator over all combinations of the C{iterables}. Each yielded
        combination is a list of size C{len(iterables)} where the i-th element
        is drawn from the i-th iterable. B{Important note:} This list should not
        be modified between iterations; if you need to modify it, copy it to a
        new container.
    
    @param iterables: One or more arbitrary iterables.
    @param kwds: Currently only 'blocksize' allowed.
    @keyword blocksize: Determines the order of the yielded combinations. By
        default (C{blocksize=1}), the first iterable corresponds to the most outer
        loop (slowest change) and the last iterable corresponds to the most inner
        loop (fastest change).
        
        For larger blocksize, each iterable is first partitioned into consecutive
        blocks of size C{blocksize} (except perhaps for the last block which may
        be shorter). Then each combination is yielded by first iterating over
        each block combination C{B := (B1,B2,..Bn)} and then yielding each
        combination from B.
        
        More generally, C{blocksize} can be an iterable so that different
        C{iterables} can be partitioned by different block size. In this case,
        C{blocksize} is repeated as many time as necessary to match C{len(iterables)}.
        For instance::
            iterCombinations(range(4),range(6),range(8),'xyz', blocksize=(2,3))
        partitions C{range(4)} and C{range(8)} with blocksize=2, while C{range(6)}
        and 'xyz' are partitioned with blocksize=3.
    '''
    combo = [None] * len(iterables)
    blocksize = kwds.get('blocksize', 1)
    if isinstance(blocksize, int):
        sizes = repeat(blocksize)
    else:
        sizes = cycle(iter(blocksize))
    block_lists = [list(_iterblocks(it,sz)) for it,sz in izip(iterables,sizes)]
    for block_combo in _iterCombinations(block_lists, [None] * len(iterables)):
        for _ in _iterCombinations(block_combo, combo):
            yield combo


def _iterCombinations(groups, combo_list, index=0):
    # generate recursively all combinations of groups, updating combo_list
    # *in-place* for each combination.    
    if index < len(groups)-1:
        for x in groups[index]:
            combo_list[index] = x
            for _ in _iterCombinations(groups,combo_list,index+1):
                yield combo_list
    else: # optimization to avoid the last level of recursion
        assert index == len(groups)-1
        for x in groups[index]:
            combo_list[index] = x
            yield combo_list

        
def _iterblocks(iterable, blocksize, factory=tuple):
    # split the iterable into blocks of blocksize
    iterable = iter(iterable)
    while True:
        block = factory(islice(iterable,blocksize))
        if not block: break
        yield block
        if len(block) < blocksize: break


# example
>>> for c in iterCombinations(range(5), 'abc'): print c
...
[0, 'a']
[0, 'b']
[0, 'c']
[1, 'a']
[1, 'b']
[1, 'c']
[2, 'a']
[2, 'b']
[2, 'c']
[3, 'a']
[3, 'b']
[3, 'c']
[4, 'a']
[4, 'b']
[4, 'c']

>>> for c in iterCombinations(range(5), 'abc', blocksize=2): print c
...
[0, 'a']
[0, 'b']
[1, 'a']
[1, 'b']
[0, 'c']
[1, 'c']
[2, 'a']
[2, 'b']
[3, 'a']
[3, 'b']
[2, 'c']
[3, 'c']
[4, 'a']
[4, 'b']
[4, 'c']
