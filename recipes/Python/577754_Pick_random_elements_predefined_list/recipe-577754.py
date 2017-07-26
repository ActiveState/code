def picker(seq):
    """
       Returns a new function that can be called without arguments 
       to select and return a random entry from the provided sequence
    """
    from functools import partial
    from random import choice

    return partial(choice,seq)
