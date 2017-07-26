def splitIterator(text, size):
    assert size > 0, "size should be > 0"
    for start in xrange(0, len(text), size):
        yield text[start:start + size]
