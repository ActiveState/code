def iter_find(_str, to_find, n=0):
    """ Finds all occurences of `to_find` in `_str`. Itering-ready. """
    _str_len = len(_str)
    to_find_len = len(to_find)
    while n <= _str_len:
        if _str[n:n+to_find_len] == to_find:
            yield n
        n += 1

def ireplace(text, old, new):
    """ Replaces as occurences of `old` with the string pattern `new`.
        The `new` variable has to be a string (additionally containing a
        placeholder where the matches go (`%s`). """
    assert(isinstance(text, str) and isinstance(old, str))
    use_string_format = '%s' in new

    old_len = len(old)
    to_replace = []
    for match in iter_find(text.lower(), old.lower()):
        match = text[match:match+old_len]
        if match not in to_replace:
            if use_string_format:
                to_replace.append((match, new % match))
            else:
                to_replace.append((match, new))
    for rule in to_replace:
        text = text.replace(*rule)
    return text
