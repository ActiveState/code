# A regular expression that matches Python string literals.
# Tripple-quoted, unicode, and raw strings are supported.  This
# regular expression should be compiled with the re.VERBOSE flag.
PY_STRING_LITERAL_RE = (r"""
[uU]?[rR]?
  (?:              # Single-quote (') strings
  '''(?:                 # Tripple-quoted can contain...
      [^']               | # a non-quote
      \\'                | # a backslashed quote
      '{1,2}(?!')          # one or two quotes
    )*''' |
  '(?:                   # Non-tripple quoted can contain...
     [^']                | # a non-quote
     \\'                   # a backslashded quote
   )*'(?!') | """+
r'''               # Double-quote (") strings
  """(?:                 # Tripple-quoted can contain...
      [^"]               | # a non-quote
      \\"                | # a backslashed single
      "{1,2}(?!")          # one or two quotes
    )*""" |
  "(?:                   # Non-tripple quoted can contain...
     [^"]                | # a non-quote
     \\"                   # a backslashded quote
   )*"(?!")
)''')

# Example use case:
def replace_identifier(s, old, new):
    """
    Replace any occurance of the Python identifier `old` with `new` in
    the given string `s` -- but do *not* modify any occurances of
    `old` that occur inside of string literals or comments.  This
    could be used, e.g., for variable renaming.
    """
    # A regexp that matches comments, strings, and `old`.
    comment_re = r'\#.*'
    regexp = re.compile(r'(?x)%s|%s|(?P<old>\b%s\b)' %
                        (comment_re, PY_STRING_LITERAL_RE, re.escape(old)))

    # A callback used to find the replacement value for each match.
    def repl(match):
        if match.group('old'):
            # We matched `old`:
            return new 
        else:
            # We matched a comment or string literal:
            return match.group()

    # Find an regexp matches, and use `repl()` to find the replacement
    # value for each.  Since re.sub only replaces leftmost
    # non-overlapping occurances, occurances of `old` inside strings
    # or comments will be matched as part of that string or comment,
    # and so won't be changed.
    return regexp.sub(repl, s)
