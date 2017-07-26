def caesar(n):
    return lambda s:("".join(map(lambda x:(chr((ord(x.lower())-97+n)%26+97)),s)))
