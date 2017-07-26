import cStringIO
import tokenize

from collections import defaultdict, deque
from decimal import Decimal
from functools import partial

__version__ = "1.1"
__author__ = "Florian Leitner"

__all__ = ["parse", "parseOne"]

# For defining the default type for the defaultdict as to not use eval(type):
# TODO: better method?
TYPES = {
    "int": int,
    "long": long,
    "float": float,
    "Decimal": Decimal,
    "bool": bool,
    "str": str,
    "list": list,
    "tuple": tuple,
    "set": set,
    "deque": deque,
    "dict": dict,
    "defaultdict": defaultdict,
    "None": None
}

def _error(tok, msg):
    raise SyntaxError("%s token(%s, '%s') at %s = from/to [row, col]"
                      % (msg, tokenize.tok_name[tok[0]],
                         tok[1], str(tok[2:4])))

_fail = partial(_error, msg="malformed expression")

def _parse(token, src):
    try:
        return _dispatcher[token[0]](token, src)
    except KeyError:
        _error(token, "unknown token type")

def _parseBool(token, src):
    # bool
    return token[1] == "True"

def _parseDecimal(token, src):
    # Decimal("number")
    _tests(src, (('(', 'open'),), "malformed Decimal")
    token = src.next()
    if token[0] != tokenize.STRING:
        _error(token, "malformed Decimal string")
    out = Decimal(token[1][1:-1])
    _tests(src, ((')', 'close'),), "malformed Decimal")
    return out

def _parseDefaultdict(token, src):
    # defaultdict(<type 'type'>, {...})
    tests = (('(', 'open'), ('<', 'typeopen'), ('type', 'typestring'))
    _tests(src, tests, "malformed defaultdict")
    token = src.next()
    try:
        dicttype = TYPES[token[1][1:-1]]
    except KeyError:
        _error(token, "unknown defaultdict type")
    tests = (('>', 'typeclose'), (',', 'typesep'))
    _tests(src, tests, "malformed defaultdict")
    dd = _parse(src.next(), src)
    if type(dd) != dict:
        _error(src.next(), "malformed defaultdict dict '%s' - next" % str(dd))
    out = defaultdict(dicttype, dd)
    _tests(src, ((')', 'close'),), "malformed defaultdict")
    return out

def _parseName(token, src):
    try:
        return _dispatchName[token[1]](token, src)
    except KeyError:
        _fail(token)

def _parseNone(token, src):
    # None
    return None

def _parseNumber(token, src):
    # int, float, long
    try:
        if token[1][-1] == "L":
            return long(token[1], 0)
        return int(token[1], 0) 
    except ValueError:
        return float(token[1])

def _parseOp(token, src):
    if token[1] == "{":
        # {dict}
        out = {}
        token = src.next()
        while token[1] != "}":
            key = _parse(token, src)
            _tests(src, ((':', 'separator'),), "malformed dictionary")
            value = _parse(src.next(), src)
            out[key] = value
            token = src.next()
            if token[1] == ",":
                token = src.next()
        return out
    elif token[1] in ("[", "("):
        # [list], (tuple)
        container = list if token[1] == "[" else tuple
        out = []
        token = src.next()
        while token[0] != tokenize.OP and token[1] not in ("]", ")"):
            out.append(_parse(token, src))
            token = src.next()
            if token[1] == ",":
                token = src.next()
        return container(out)
    else:
        _fail(token)

def _parsePass(token, src):
    # just continue...
    return _parse(src.next(), src)

def _parseSet(token, src):
    # set([...]), deque([...])
    container = set if token[1] == "set" else deque
    name = token[1]
    _tests(src, (('(', 'open'),), "malformed %s" % name)
    lst = _parse(src.next(), src)
    if type(lst) != list:
        _error(src.next(), "malformed %s list '%s' - next" % (name, str(lst)))
    _tests(src, ((')', 'close'),), "malformed %s" % name)
    return container(lst)

def _parseString(token, src):
    # str
    return token[1][1:-1].decode("string-escape")

def _tests(src, tests, base_msg):
    for sym, msg in tests:
        token = src.next()
        if token[1] != sym:
            _error(token, "%s %s" % (base_msg, msg))
    return


def _tokenize(source):
    src = cStringIO.StringIO(source).readline
    return tokenize.generate_tokens(src)

_dispatcher = {
    tokenize.ENDMARKER: _parsePass,
    tokenize.INDENT: _parsePass,
    tokenize.NAME: _parseName,
    tokenize.NL: _parsePass,
    tokenize.NEWLINE: _parsePass,
    tokenize.NUMBER: _parseNumber,
    tokenize.OP: _parseOp,
    tokenize.STRING: _parseString,
}

_dispatchName = {
    "set": _parseSet,
    "deque": _parseSet,
    "defaultdict": _parseDefaultdict,
    "Decimal": _parseDecimal,
    "None": _parseNone,
    "True": _parseBool,
    "False": _parseBool,
}

def parse(source):
    """ Parses a type string to their type objects for all basic types.
        
        Yields [nested] type objects.
        
        Raises SyntaxError and SemanticError on failures.
        
        Supported types:
        * containers: defaultdict, deque, dict, list, tuple, set
        * basic types: Decimal, bool, float, int, long, str
        * None type
    """
    src = _tokenize(source)
    for token in src:
        yield _parse(token, src)

def parseOne(source):
    """ Parses only the next type object from source and returns it together
        with the remaining [possibly empty] string as an object, string tuple.
    """
    src = _tokenize(source)
    obj = _parse(src.next(), src)
    try:
        next = src.next()
    except StopIteration:
        rest = ""
    else:
        rest = source.split('\n')[next[2][0] - 1:]
        if len(rest) == 0:
            rest = ""
        else:
            rest[0] = rest[0][next[2][1]:]
            rest = '\n'.join(rest)
    finally:
        return obj, rest
