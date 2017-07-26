def hashed_float(s):
    """returns a float in the range [0, 1) based on a hash of the string.
    A given string will always return the same value, but different strings
    will return very different values."""
    import md5, struct
    [number] = struct.unpack("<H", md5.new(s).digest()[:2])
    return number / float(0xFFFF)
