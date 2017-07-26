"""Parse files stored in the RFC 822 metaformat."""

from extensions.itertools import two_finger
from re import compile as Regex

def lines(string):
    """Get the logical lines of the string."""
    return merge_lines(string.splitlines())

def load(string):
    """Parse the given string."""
    return pairs(remove_comments(lines(string)))

def merge_lines(lines):
    """Merge every line that begins with whitespace with its predecessor.  May
    raise a ParseError."""
    new_lines = []
    offset = 0
    for offset, line in enumerate(lines):
        if len(line) > 0 and not line.isspace():
            break
    lines = lines[offset:]
    if starts_with_whitespace(lines[0]):
        raise ParseError("%d: '%s': Keys cannot be indented.")
    for line in lines:
        if starts_with_whitespace(line):
            new_lines[-1] += line
        else:
            new_lines.append(line)
    return [line.strip() for line in new_lines]

def pairify(string):
    """Convert a string of the form "key: value" to a tuple ("key",
    "value").  May raise a ParseError."""
    items = string.split(":", 1)
    try:
        return items[0].strip(), items[1].strip()
    except IndexError:
        raise ParseError("'%s': Keys must be terminated with a colon." %
                         string)

def pairs(lines):
    """Convert a list of lines into a dictionary.  May raise a ParseError."""
    return dict(pairify(line) for line in lines)

def remove_comments(lines):
    """Remove all lines containing a comment."""
    comment_line = Regex("^\s*#.*$")
    eol_comment = Regex(r"(?<!\\)#.*$")
    return [eol_comment.sub("", line) for line in lines if not comment_line.match(line)]

def starts_with_whitespace(line):
    return len(line) == 0 or line[0].isspace()

class ParseError(Exception): pass
