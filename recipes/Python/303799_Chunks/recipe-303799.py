def chunks(thing, chunk_length):
    """Iterate through thing in chunks of size chunk_length.

    Note that the last chunk can be smaller than chunk_length.
    """
    for i in xrange(0, len(thing), chunk_length):
        yield thing[i:i+chunk_length]
