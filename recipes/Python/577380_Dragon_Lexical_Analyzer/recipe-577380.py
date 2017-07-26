import sys
import os

EOF = ""

def get_num():
    digits = []
    t = getchar()
    while t.isdigit():
        digits.append(t)
        t = getchar()
    if t != EOF: 
        ungetc(t)
    num = int("".join(digits))
    return num

def get_word():
    chars = []
    t = getchar()
    while t.isalnum():
        chars.append(t)
        t = getchar()
    if t != EOF: 
        ungetc(t)
    s = "".join(chars)
    return s

class DragonException(Exception):
    pass

class Tag(object):
    NONE = -1
    NUM = 256
    DIV = 257
    MOD = 258
    ID = 259
    DONE = 260    
    
class Token(object):
    def __init__(self, t, value=''):
        self.tag = t
        self.value = value
        
    def __str__(self):
        return "Token([%s] [%s])" % (str(self.tag), str(self.value))
    
class Num(Token):
    def __init__(self, v):
        Token.__init__(self, Tag.NUM, v)
      
class Word(Token):
    def __init__(self, tag, lexeme):
        Token.__init__(self, tag, lexeme)

class Lexer(object):
    def __init__(self):
        self.lineno = 0
        self.lookahead = None
        self.out = []
        self.sym_table = {}  # symbol table: lexeme -> token tag
        self.insert("div", Tag.DIV)
        self.insert("mod", Tag.MOD)
            
    def lookup(self, key):
        return self.sym_table.get(key, None)
       
    def insert(self, key, tag):
        self.sym_table[key] = tag
       
    def parse(self):
        self.lookahead = self.lexan()
        while self.lookahead.tag != Tag.DONE:
            self.expr()
            self.match(';')
        return self

    def lexan(self):
        token = None
        while not token:
            t = getchar()
            if t == ' ' or  t == '\t':
                pass # strip out white space
            elif t == '\n':
                self.lineno += 1
            elif t.isdigit():
                ungetc(t)
                num = get_num()
                token = Num(num)       
            elif t.isalpha():
                ungetc(t)
                word = get_word()
                tag = self.lookup(word) 
                if not tag:
                    tag = Tag.ID
                    self.insert(word, tag)
                token = Word(tag, word)
            elif t == EOF:
                token = Token(Tag.DONE)
            else:
                token = Token(t)
        return token
            
    def expr(self):
        self.term()
        while True:
            token = self.lookahead
            if token.tag == '+' \
                    or token.tag == '-':
                self.match(token.tag)
                self.term()
                self.emit(token)
            else:
                break
            
    def term(self):
        self.factor()
        while True:
            token = self.lookahead
            if token.tag == '*' \
                    or token.tag == '/' \
                    or token.tag == Tag.DIV \
                    or token.tag == Tag.MOD:
                self.match(token.tag)
                self.factor()
                self.emit(token)
            else:
                break
            
    def factor(self):
        token = self.lookahead
        if token.tag == '(':
            self.match('(')
            self.expr()
            self.match(')')
        elif token.tag == Tag.NUM:
            self.emit(token)
            self.match(Tag.NUM)
        elif token.tag == Tag.ID:
            self.emit(token)
            self.match(Tag.ID)
        else:
            raise DragonException("factor: bad token tag - %s" % token)
        
    def match(self, tag):
        if self.lookahead.tag == tag:
            self.lookahead = self.lexan()
        else:
            raise DragonException("match: tag %s doesn't match %s" % (tag, self.lookahead))

    def emit(self, token):
        tag = token.tag
        value = token.value
        if tag == '+' or tag == '-' or tag == '*' or tag == '/':
            out = "%s" % tag
        elif tag == Tag.DIV:
            out = "DIV"
        elif tag == Tag.MOD:
            out = "MOD"
        elif tag == Tag.NUM:
            out = "%d" % value
        elif tag == Tag.ID:
            out = "%s" % value
        else:
            out = "emit: %s" % (token)
            
        self.out.append(out)
        print out
            
    def db(self, intro=""):
        print "%s %s" % (intro,  self.lookahead)
        
def main():
    lex = Lexer().parse()
    print lex.out

# python specific
import StringIO

FP = None
def getchar():
    if FP:
        return FP.read(1)
    
def ungetc(c=''):
    if FP:
        FP.seek(-1, os.SEEK_CUR)    
        
SRC = """1 + (2 + 3);
4 * (5 + 6);
7 div (8 - 9);
10 mod (11 + 12);
"""

if __name__ == "__main__":
    FP = StringIO.StringIO(SRC)
    main()
