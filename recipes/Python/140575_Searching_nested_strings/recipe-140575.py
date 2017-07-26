from mx.TextTools import *

text = "aa(AA)a((BB))aa((CC)DD)aa(EE(FF))aa(GG(HH(II)JJ)KK)aa"

tables = []

tab = ('start',
       (None,Is+LookAhead,'(',+1,'nesting'), # If next character is "(" then recurse
       (None,Is,')',+1,MatchOk), # If current character is ")" then stop or return from recursion
       (None,AllNotIn,'()',+1,'start'), # Search all characters except "(" and ")"
       (None, EOF, Here, MatchOk),
       'nesting',
       ('group',SubTable+AppendMatch,((None,Is,'(',0,+1), # Since we have looked ahead, collect "(" -sign
                                      (None,SubTableInList, (tables,0)))), # Recurse
       (None,Jump,To,'start')) # After recursion jump back to 'start'

tables.append(tab) # Add tab to tables

if __name__ == '__main__':

    result, taglist, nextindex = tag(text,tab)
    print taglist


-----the version below returns strings without limiting characters ----


from mx.TextTools import *

text = "aa(AA)a((BB))aa((CC)DD)aa(EE(FF))aa(GG(HH(II)JJ)KK)aa"

tab = ('start',
       (None, Is+LookAhead, ')', +1, MatchOk),
       (None, Is, '(', 'letters', +1),
       ('group', SubTable+AppendMatch, ThisTable),
       (None, Skip, 1, MatchFail, 'start'),
       'letters',
       (None, AllNotIn, '()', +1, 'start'),
       (None, EOF, Here, MatchOk))

result,taglist,next = tag(text, tab)
print taglist
