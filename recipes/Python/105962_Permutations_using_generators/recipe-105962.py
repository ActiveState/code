def permIter(seq):
    """Given some sequence 'seq', returns an iterator that gives
    all permutations of that sequence."""
    ## Base case
    if len(seq) == 1:
        yield(seq[0])
        raise StopIteration

    ## Inductive case
    for i in range(len(seq)):
        element_slice = seq[i:i+1]
        rest_iter = permIter(seq[:i] + seq[i+1:])
        for rest in rest_iter:
            yield(element_slice + rest)
    raise StopIteration
