import re

class REstr(str):

    cache = {}

    def __div__(self, regex):
        try:
            reg = REstr.cache[regex]
        except KeyError:
            REstr.cache[regex] = reg = re.compile(regex)
        self.sre = reg.search(self)
        return REstr(self.sre.group())
        
    def __idiv__(self, tpl):
        try:
            regex, repl, count = tpl
        except ValueError:
            regex, repl = tpl
            count = 0
        try:
            reg = REstr.cache[regex]
        except KeyError:
            REstr.cache[regex] = reg = re.compile(regex)
        return REstr(reg.sub(repl, self, count))

    def __call__(self, g):
        return self.sre.group(g)

if __name__ == '__main__':
    a = REstr('abcdebfghbij')
    print "a :", a

    print "Match a / 'b(..)(..)' :",
    print a / 'b(..)(..)'               # find match

    print "a[0], a[1], a[2] :",
    print a[0], a[1], a[2]              # print letters from string

    print "a(0), a(1), a(2) :",
    print a(0), a(1), a(2)              # print matches

    print "a :", a

    a /= 'b.', 'X', 1                   # find and replace once
    print "a :", a

    a /= 'b.', 'X'                      # find and replace all
    print "a :", a
