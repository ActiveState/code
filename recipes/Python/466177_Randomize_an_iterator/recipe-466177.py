def irandomize(iterable, seed=None):
    """
    Randomize the iterable.

    Note: this evaluates the entire iterable to a sequence in memory
    """
    if seed is None:
        from random import shuffle
    else:
        from random import Random
        shuffle = Random(seed).shuffle
    result = list(iterable)
    shuffle(result)
    return iter(result)

if __name__ == "__main__":
    print list(irandomize(range(10)))
    print list(irandomize(range(10)))
    print list(irandomize(range(10), seed=14))
    print list(irandomize(range(10), seed=14))
