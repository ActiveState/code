"""simplified extension of the replace function in python"""

def replacen(text, kwargs):
    """any single character of `text` in `kwarg.keys()` is replaced by `kwarg[key]`
    >>> consonants = replacen('abcdefghijklmnopqrstuvwxyz', {'aeiou':''})
    """
    
    try:
        text = [str(i) for i in text]
    except (ValueError, TypeError):
        raise TypeError("`text` parameter must have valid str type")
        
    #check the contents of each key, make sure there's no overlap:
    collisions = any_key_collisions(kwargs)
    if collisions:
        raise KeyError("keys have duplicate find-replace strings: '%s'" % collisions)
    
    #bring all keys together during character comparisons
    all_keys = [[ix for ix in i] for i in kwargs.keys()]
    for idx, i in enumerate(text):
        for key in all_keys:
            if i in ''.join(key):
                text[idx] = kwargs.get(''.join(key))
    return ''.join(text)

def any_key_collisions(dictionary):
    """ensures no keys contain any other key element, across all keys"""
    members = [i for i in dictionary.keys()]
    dups = []
    for idx, _ in enumerate(members):
        candidate = members[idx * -1]
        if candidate in members[: idx * -1]:
            dups.append(candidate)
    return ''.join(set(dups))
    
if __name__ == '__main__':
    original = "\"This is a quote, 'from a famous book'.\""
    no_punc = replacen(original, {'"\'.' : '', ',': ' --'})
    print original, '\n', no_punc
