import random

def scramble(string):
    """Scramble and return a string, preserving spaces."""
    return ' '.join([''.join(random.sample(word, len(word))) for word in string.split()])
