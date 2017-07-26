def enum(names):
    "Create a simple enumeration having similarities to C."
    return type('enum', (), dict(map(reversed, enumerate(
        names.replace(',', ' ').split())), __slots__=()))()
