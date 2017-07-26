def grep(*matches):
    """Returns a generator function that operates on an iterable:
        filters items in the iterable that match any of the patterns.

    match: a callable returning a True value if it matches the item

    >>> import re
    >>> input = ["alpha\n", "beta\n", "gamma\n", "delta\n"]
    >>> list(grep(re.compile('b').match)(input))
    ['beta\n']
    """
    def _do_grep_wrapper(*matches):
        def _do_grep(lines):
            for line in lines:
                for match in matches:
                    if match(line):
                        yield line
                        break
        return _do_grep
    return _do_grep_wrapper(*matches)
