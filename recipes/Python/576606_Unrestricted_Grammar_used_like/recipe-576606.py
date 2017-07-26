#!/usr/bin/python
#
# unresistricted grammar with dictionary interface
# v.01
# Written by Shea Kauffman
#
# based upon the thue langauage by: 
# John Colagioia 
# and the interpreter by:
# Frederic van der Plancke
#
#

import string

def find_all(s, pattern):
    """return ordered list of indexes where [pattern] appears in [s];
    """
    shift_on_match = 1
    i = 0
    indexes = []
    while 1:
        i = string.find(s, pattern, i)
        if i >= 0:
            indexes.append(i)
            i = i + shift_on_match
        else:
            break
    return indexes

class Rule:
    def __init__(self, lhs, rhs, output=None):
        self.lhs = lhs
        self.rhs = rhs
        self.output = output  # UNUSED in current version

    def __str__(self):
        return "%s :- %s" % (self.lhs, self.rhs)

    def __repr__(self):
        return "Rule(%s,%s)" % (repr(self.lhs), repr(self.rhs))

class grammar:
    def __init__(self):
        self.rulebase = []
        self.trace = False        

    def __call__(self, item): 
        while self[item] != item:
            item = self[item]
        return item

    def __getitem__(self, tape):
        matches = []
        for rule in self.rulebase:
            indices = find_all(tape, rule.lhs)
            for i in indices:
                matches.append((i, rule))
        if len(matches) == 0:
            if self.trace:
                print tape
            return tape
#        print matches
        (pos, rule) = min(matches)
        endpos = pos + len(rule.lhs)
        dataspace = tape[ : pos] + rule.rhs + tape[endpos : ]
        if self.trace:
            print tape, '->', dataspace
        return dataspace

    def __setitem__(self, lhs, rhs): 
        self.rulebase.append(Rule(lhs, rhs))

    def __repr__(self):
        ret = ''
        for rule in self.rulebase:
            ret = ret+'\n'+rule.__str__()
        return ret

if __name__ == '__main__':
    #TESTS:
    #t1
    t1 = grammar()
    t1['ZZZ'] = '...'
    
    #t2
    t2 = grammar()
    t2['0_']='0--'
    t2['1_']='0'
    t2['10--']='01'
    t2['00--']='0--1'
    t2['_1--']='@'
    t2['_0--']='1'
    t2['_0']=''

    #t3
    t3 = grammar()
    t3['__']='Hello, World!'

    #t4
    t4 = grammar()
    t4['1_']='1++'
    t4['0_']='1'
    t4['01++']='10'
    t4['11++']='1++0'
    t4['_0']='_'
    t4['_1++']='10'

    #t5
    t5 = grammar()
    t5['_+_'] = '<+|+>'
    t5['+>0'] = '0?+>'
    t5['+>1'] = '1?+>'
    t5['+>_'] = '<@0C_'
    t5['0<+'] = '<+0?'
    t5['1<+'] = '<+1?'
    t5['_<+'] = '_'
    t5['0@0?'] = '0?0@'
    t5['0@1?'] = '1?0@'
    t5['1@0?'] = '0?1@'
    t5['1@1?'] = '1?1@'
    t5['0@|'] = '|0@'
    t5['1@|'] = '|1@'
    t5['0@0@0C'] = '<@0C0'
    t5['0@0@1C'] = '<@0C1'
    t5['0@1@0C'] = '<@0C1'
    t5['0@1@1C'] = '<@1C0'
    t5['1@0@0C'] = '<@0C1'
    t5['1@0@1C'] = '<@1C0'
    t5['1@1@0C'] = '<@1C0'
    t5['1@1@1C'] = '<@1C1'
    t5['0?<@'] = '<?0@'
    t5['1?<@'] = '<?1@'
    t5['0?<?'] = '<?0?'
    t5['1?<?'] = '<?1?'
    t5['|<?'] = '<@|'
    t5['_<?'] = '_'
    t5['0?|<@'] = '|0@0@'
    t5['1?|<@'] = '|1@0@'
    t5['_<@|'] = '_|0@'
    t5['_|<@'] = '_'
    t5['_0C'] = '_'
    t5['_1C'] = '_1'

    t1.trace = True
    print t1
    assert t1('ZZZZZZZZZZZZ') == '............'
    
    t2.trace = True
    print t2
    assert t2('_1000000000000_') == '111111111111'
    
    t3.trace = True
    print t3
    assert t3('__') == 'Hello, World!'
    
    t4.trace = True
    print t4
    assert t4('_1111111111_') == '10000000000'
    
    t5.trace = True
    print t5
    assert t5('_111100_+_10010_') == '_1001110_'
    
    d = grammar()
    d["server"]="mpilgrim"
    d["database"]="master"
    print d["server"]                       # mpilgrim
    print d["database"]                     # master
    print d["server is offline"]            # mpilgrim is offline
    print d["database server is offline"]   # master server is offline
    print d("database server is offline")   # master mpilgrim is offline
