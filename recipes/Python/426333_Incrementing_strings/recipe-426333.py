def inc_string(string, allowGrowth=True):
    '''Increment a string.'''
    CHAR_RANGES = [
                   Bunch(from_char=ord('0'), to_char=ord('9')), # digits
                   Bunch(from_char=ord('A'), to_char=ord('Z')), # upper case
                   Bunch(from_char=ord('a'), to_char=ord('z')), # lower case
                  ]
    string_chars = list(string)
    string_chars[-1] = chr(ord(string_chars[-1]) + 1)
    for index in range(-1, -len(string_chars), -1):
        for char_range in CHAR_RANGES:
            if ord(string_chars[index]) == char_range.to_char + 1:
                string_chars[index] = chr(char_range.from_char)
                string_chars[index-1] = chr(ord(string_chars[index-1]) + 1)
    for char_range in CHAR_RANGES:
        if ord(string_chars[0]) == char_range.to_char + 1:
            if allowGrowth:
                string_chars[0] = chr(char_range.from_char)
                string_chars.insert(0, chr(char_range.from_char))
            else:
                raise ValueError, string + " cannot be incremented."
    return ''.join(string_chars)
