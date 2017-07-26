import re


scan = re.compile(flags=re.VERBOSE, pattern=r"""
    (?P<number> \d+\.?\d* ) |
    (?P<operator> \+ | - | \* | / ) |
    (?P<eof> $ ) |
    (?P<error> \S )  # catch all (except whitespace)
""").finditer


def parse(source):
    parser = RPNParser()
    for each in scan(source):
        dispatch = getattr(parser, each.lastgroup)
        dispatch(each.group())
    return parser.stack[0]


class RPNParser(object):

    def __init__(self):
        self.stack = []

    def number(self, token):
        self.stack.append(token)

    def operator(self, token):
        right = self.stack.pop()
        left = self.stack.pop()
        self.stack.append(Expression(left, token, right))

    def eof(self, token):
        if len(self.stack) != 1:
            raise Exception("source kaputt!")

    def error(self, token):
        raise Exception("unknown token %s!" % token)


class Expression(object):

    def __init__(self, *args):
        self.args = args

    def __str__(self):
        return "(%s %s %s)" % self.args


if __name__ == "__main__":

    print parse("1.5 2 + 3.33 1.11 - *")
