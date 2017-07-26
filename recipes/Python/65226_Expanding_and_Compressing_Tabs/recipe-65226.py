# of course, in Python, we do have a built-in tab expansion string method:
# method .expandtabs(tablen=8) of string objects!  If we *didn't* have
# it, though, here's how we might make it ourselves...:

# string processing tends to be faster in a split/process/rejoin
# approach than by repeated overall-string transformations, so...:
def expand_with_re(astring, tablen=8):
    import re
    pieces = re.split(r'(\t)', astring)
    lensofar = 0
    for i in range(len(pieces)):
        if pieces[i]=='\t':
            pieces[i] = ' '*(tablen-lensofar%tablen)
        lensofar += len(pieces[i])
    return ''.join(pieces)

# note we used re.split, rather than plain string splitting, because
# re.split with a '(group)' in the re gives us the splitters too,
# which is quite handy here for us to massage the pieces list into
# our desired form for the final ''.join.  However, '\t'.split,
# "interleaving" the blank joiners, looks a bit better still:
def expand(astring, tablen=8):
    result = []
    for piece in astring.split('\t'):
        result.append(piece)
        result.append(' '*(tablen-len(piece)%tablen))
    return ''.join(result[:-1])

# for the 'unexpanding', though, the "joiners" (spaces) are
# really crucial, so let's go back to the re approach (and
# _here_ we don't have a built-in method of strings...!):
def unexpand(astring, tablen=8):
    import re
    pieces = re.split(r'( +)', astring)
    lensofar = 0
    for i in range(len(pieces)):
        thislen = len(pieces[i])
        if pieces[i][0]==' ':
            numblanks = (lensofar+thislen)%8
            numtabs = (thislen-numblanks+7)/8
            pieces[i] = '\t'*numtabs + ' '*numblanks
        lensofar += thislen
    return ''.join(pieces)
