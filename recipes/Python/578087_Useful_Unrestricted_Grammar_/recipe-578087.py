#!/usr/bin/env python
#
# unresistricted grammar with dictionary interface
# v.11
# Written by Shea Kauffman
#
# based upon the thue langauage by: 
# John Colagioia 
# and the interpreter by:
# Frederic van der plancke
#
#

import string, re

def find_all(s, pattern):
    """
    return ordered list of indexes where [pattern] appears in [s];
    """
    shift_on_match = 1
    indexes = []
    i = re.search(pattern, s)
    if i:
        i, j, k = i.start(), i.end(), i.groups()
        indexes.append((i,j,k))
    return indexes

class Rule:
    def __init__(self, lhs, rhs, output=None):
        self.lhs = lhs
        self.rhs = rhs

    def __str__(self):
        return "%s :- %s" % (self.lhs, self.rhs)

    def __repr__(self):
        return "Rule(%s,%s)" % (repr(self.lhs), repr(self.rhs))

class grammar(object):
    rulebase = ()
    
    def __init__(self, rules=()):
        self.rulebase = tuple(rules)
        self.trace = False   

    def __call__(self, item): 
        prev = None
        while prev != item:
            prev = item
            item = self[item]
        return item

    def __getitem__(self, tape):
        (match, rule) = self._matches(tape)
        if not match:
            '''If there are no matches then we're done'''
            if self.trace: print tape
            return tape
        startpos, endpos, matched = match
        middledata = self._transform(matched, rule)
        dataspace = tape[ : startpos] + middledata + tape[endpos : ]
        if self.trace:
            print tape, '->', dataspace, '\t\t::\t', rule
        return dataspace

    def __setitem__(self, lhs, rhs): 
        self.rulebase = self.rulebase + (Rule(lhs, rhs), )

    def __repr__(self):
        return '\n'.join([rule.__str__() for rule in self.rulebase])

    def __add__(self, other):
        newg = grammar(self.rulebase+other.rulebase)
        newg.trace = self.trace and other.trace
        return newg
        
    def _matches(self, tape):
        '''iterate through rules returning first match'''
        for rule in self.rulebase:
            for i in find_all(tape, rule.lhs):
                return i, rule
        return False, None
    
    def _transform(self, matched, rule):
        if not matched:
            return rule.rhs  
        return rule.rhs(*matched) if callable(rule.rhs) else rule.rhs % matched
        
if __name__ == '__main__':
    TRACES = True
    #TESTS:
    #lengthdiv3
    lengthdiv3 = grammar()
    lengthdiv3['ZZZ'] = '...'
    lengthdiv3.trace = TRACES
    assert lengthdiv3('ZZZZZZZZZZZZ') == '............'
    
    #bitshift
    bitshift = grammar()
    bitshift['0_']='0--'
    bitshift['1_']='0'
    bitshift['10--']='01'
    bitshift['00--']='0--1'
    bitshift['_1--']='@'
    bitshift['_0--']='1'
    bitshift['_0']=''
    bitshift.trace = TRACES
    assert bitshift('_1000000000000_') == '111111111111'

    #helloworld
    helloworld = grammar()
    helloworld['__']='Hello, World!'
    helloworld.trace = TRACES
    assert helloworld('__') == 'Hello, World!'

    #binarysucc
    binarysucc = grammar()
    binarysucc['1_']='1++'
    binarysucc['0_']='1'
    binarysucc['01\+\+']='10'
    binarysucc['11\+\+']='1++0'
    binarysucc['_0']='_'
    binarysucc['_1\+\+']='10'
    binarysucc.trace = TRACES
    assert binarysucc('_1111111111_') == '10000000000'

    #binaryadd
    binaryadd = grammar()
    binaryadd[r'_\+_'] = '<+|+>'
    binaryadd[r'\+\>0'] = '0?+>'
    binaryadd[r'\+\>1'] = '1?+>'
    binaryadd[r'\+\>_'] = '<@0C_'
    binaryadd[r'0\<\+'] = '<+0?'
    binaryadd[r'1\<\+'] = '<+1?'
    binaryadd[r'_\<\+'] = '_'
    binaryadd[r'0\@0\?'] = '0?0@'
    binaryadd[r'0\@1\?'] = '1?0@'
    binaryadd[r'1\@0\?'] = '0?1@'
    binaryadd[r'1\@1\?'] = '1?1@'
    binaryadd[r'0\@\|'] = '|0@'
    binaryadd[r'1\@\|'] = '|1@'
    binaryadd[r'0\@0\@0C'] = '<@0C0'
    binaryadd[r'0\@0\@1C'] = '<@0C1'
    binaryadd[r'0\@1\@0C'] = '<@0C1'
    binaryadd[r'0\@1\@1C'] = '<@1C0'
    binaryadd[r'1\@0\@0C'] = '<@0C1'
    binaryadd[r'1\@0\@1C'] = '<@1C0'
    binaryadd[r'1\@1\@0C'] = '<@1C0'
    binaryadd[r'1\@1\@1C'] = '<@1C1'
    binaryadd[r'0\?\<\@'] = '<?0@'
    binaryadd[r'1\?\<\@'] = '<?1@'
    binaryadd[r'0\?\<\?'] = '<?0?'
    binaryadd[r'1\?\<\?'] = '<?1?'
    binaryadd[r'\|\<\?'] = '<@|'
    binaryadd[r'_\<\?'] = '_'
    binaryadd[r'0\?\|\<\@'] = '|0@0@'
    binaryadd[r'1\?\|\<\@'] = '|1@0@'
    binaryadd[r'_\<\@\|'] = '_|0@'
    binaryadd[r'_\|\<\@'] = '_'
    binaryadd[r'_0C'] = '_'
    binaryadd[r'_1C'] = '_1'
    binaryadd.trace = TRACES
    assert binaryadd('_111100_+_10010_') == '_1001110_'
    
    palindrome = grammar()
    palindrome[r'(?:^1)([01]*)(?:1$)'] = '%s'
    palindrome[r'(?:^0)([01]*)(?:0$)'] = '%s'
    palindrome[r'^1$'] = ''
    palindrome[r'^0$'] = ''
    palindrome.trace = True
    assert palindrome('000111000') == ''
    assert palindrome('000101000') == ''
    assert palindrome('0001110') == '00111'
    assert palindrome('101100101') == '100'
    
    
    dictionary = grammar()
    dictionary["database"]="master"
    dictionary["server"]="mpilgrim"
    dictionary.trace = TRACES
    
    assert dictionary["server"] == 'mpilgrim'
    assert dictionary["database"] == 'master'
    assert dictionary["server is offline"] == 'mpilgrim is offline'
    assert dictionary["database server is offline"] == 'master server is offline'
    assert dictionary("database server is offline") == 'master mpilgrim is offline'

    #print re.search(r"(\w+)\+(\w+)", "3+6", 1).groups()

    addition = grammar()
    addition.trace = TRACES
    addition[r'(\w+)\+(\w+)'] = '+(%s, %s)'
    addition[r'\+\((\w+), (\w+)\)'] = lambda x,y: str(int(x)+int(y))
    assert addition('2+3') == '5'
    assert int(addition('26435+33333')) == 26435+33333
    
    multiply = grammar()
    multiply.trace = TRACES
    multiply[r'(\w+)\s*\*\s*(\w+)'] = '*(%s, %s)'
    multiply[r'\*\((\w+),\s*(\w+)\)'] = lambda x,y: str(int(x)*int(y))
    assert multiply('2*3') == '6'
    assert int(multiply('26435*33333')) == 26435*33333
    
    math = multiply+addition
    math['\((\w+)\)'] = lambda x: math(x) #recursive step
    math.trace = TRACES
    assert int(math('26435*33333')) == 26435*33333
    assert int(math('(26435+26435)*33333')) == (26435+26435)*33333
    assert int(math('26435+(26435*33333)')) == 26435+(26435*33333)
    assert math('26435+(26435*33333)') == math('26435+26435*33333')
    
        
    
    whitespace = grammar()
    whitespace.trace = TRACES
    whitespace['\n(?P<ws>\s+)(.*)(?P=ws)'] = lambda x,y: ',%s' % y 
    whitespace['\|,(.*)'] = lambda x: 'where(%s)' % x 
    
    assert whitespace('''
z = y |
    baz = bar
    foo = blurk
    moo = cow
''').strip() == 'z = y where(baz = bar,foo = blurk,moo = cow)'
    assert whitespace('''
z = y |
    baz = bar |
        foo = blurk
        moo = cow
''').strip() == 'z = y where(baz = bar where(foo = blurk,moo = cow))'
    assert whitespace('''
z = y |
    baz = bar
    foo = blurk
    moo = cow
z = y |
    baz = bar |
        foo = blurk
        moo = cow
''').strip() == '''
z = y where(baz = bar,foo = blurk,moo = cow)
z = y where(baz = bar where(foo = blurk,moo = cow))'''.strip()
    
