"""Monad combinators for a list/generator monad in Python"""

from itertools import chain

# Infix class by Ferdinand Jamitzky

class Infix:
  def __init__(self, function):
      self.function = function
  def __ror__(self, other):
      return Infix(lambda x, self=self, other=other: self.function(other, x))
  def __or__(self, other):
      return self.function(other)
  def __call__(self, value1, value2):
      return self.function(value1, value2)


# Monad bind, return, fail and zero

@Infix
def bind(g, f):
    for v in g:
        for v2 in f(v):
            yield v2


@Infix
def mplus(g1, g2):
    return chain(g1, g2)


mzero = (v for v in [])

fail = lambda _ : mzero

mreturn = lambda x : (v for v in [x])

# Ambiguous parser example from
# http://www.nomaware.com/monads/html/listmonad.html

class Parsed:
    DIGIT="Digit"
    HEX="Hex"
    WORD="Word"
    def __init__(self, tokenType, tokenValue):
        self.tokenType = tokenType
        self.tokenValue = tokenValue

    def __repr__(self):
        return "(%s, %s)" % (self.tokenType, str(self.tokenValue))


def parseHexDigit(parsed, char):
    if parsed.tokenType==Parsed.HEX:
        val = "0123456789ABCDEF".find(char)
        if val>-1:
            return mreturn(Parsed(Parsed.HEX,
                                  (parsed.tokenValue * 16) + val))
        else:
            return mzero
    else:
        return mzero


def parseDigit(parsed, char):
    if parsed.tokenType==Parsed.DIGIT:
        if char.isdigit():
            return mreturn(Parsed(Parsed.DIGIT,
                                  (parsed.tokenValue * 10) + int(char)))
        else:
            return mzero
    else:
        return mzero


def parseWord(parsed, char):
    if parsed.tokenType==Parsed.WORD:
        if char.isalpha():
            return mreturn(Parsed(Parsed.WORD,
                                  parsed.tokenValue + char))
        else:
            return mzero
    else:
        return mzero

    
def parse(parsed, char):
    return parseHexDigit(parsed, char) |mplus| parseDigit(parsed, char) |mplus| parseWord(parsed, char)


def foldM(p, v, i):
    c = i[:1]
    cs = i[1:]
    if len(i)==1:
        return p(v, c)
    else:
        return p(v, c) |bind| (lambda r : foldM(p, r, cs))


def parseArg(string):
    hexParser = mreturn(Parsed(Parsed.HEX, 0))
    digitParser = mreturn(Parsed(Parsed.DIGIT, 0))
    wordParser = mreturn(Parsed(Parsed.WORD, ""))
    parser = hexParser |mplus| digitParser |mplus| wordParser
    return parser |bind| (lambda v : foldM(parse, v, string))
