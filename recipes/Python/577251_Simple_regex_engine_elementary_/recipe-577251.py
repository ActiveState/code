ANYCHAR = '.'; ESCAPE = '\\'
REGIONA = '['; REGIONO = ']'; RANGE = '-'; COMPLEMENT = '^'
GROUPA = '(' ; GROUPO = ')'; ALTERNATIVE = '|'
PERHAPS = '?' ; STAR = '*'; JUST_ONE_and_STAR = '+'
EXTENSION = '(?'; SKIPSTORE = '?:'

def match_region(ch, pattern):
    """ region: a list of comparation chars and ranges in [] or [^]"""
    if pattern[1]==COMPLEMENT: booly=False; booln=True; i=2
    else: booly=True; booln=False; i=1
    while i < len(pattern):
        if pattern[i]==ESCAPE:
            if pattern[i+1]==ch: return booly
            else: i+=2
        elif i<len(pattern)-2 and pattern[i+1]==RANGE:
            if pattern[i]<=ch<=pattern[i+2]: return booly
            else: i+=2
        elif pattern[i]==ch: return booly
        else: i+=1
    return booln

def match_simple_token(sarg, i, token):
    global MATCHLEN; c0=token[0]; ch=sarg[i]
    if c0==ESCAPE:
        c1=token[1]
        if c1=='s' and ch in (' ','\t','\r','\n','\f','\v'): MATCHLEN=1; return True
        elif c1=='S' and ch not in (' ','\t','\r','\n','\f','\v'): MATCHLEN=1; return True
        elif '0'<=c1<='9':
            captured=xGroups[int(c1)]; lg=len(captured)
            if sarg[i:i+lg]==captured: MATCHLEN=lg; return True        
        elif ch==c1: MATCHLEN=1; return True
    elif c0==REGIONA and match_region(ch,token): MATCHLEN=1; return True
    elif c0==ANYCHAR or c0==ch: MATCHLEN=1; return True
    return False

def strip_groupattris(s):
    if any([s.startswith(EXTENSION+c) for c in (':','=','!')]): s=s[3:]
    else: s=s[1:]
    if not s.endswith(')'): return s[:-2]
    return s[:-1]

TokenListCache = {}; xGroups = []

def parse_pattern(pattern, nested):
    """ 
    tokens are: 
    1. patterns included in brackets (parsing is recursive)
    2. regions
    3. \\ together with the escaped character
    4. periods
    5. simple characters
    All paired to 2-tuples with their trailing quantifiers or None
    """
    if pattern in TokenListCache.keys(): return TokenListCache[pattern]
    tokens=[]; i=0; pL = len(pattern)
    while i < pL:
        c = pattern[i]
        if c==REGIONA:
            k = pattern.find(REGIONO, i)
            if k==-1: raise ValueError('Unmatched '+REGIONA+' in '+pattern)
            while pattern[k-1] == ESCAPE:
                k = pattern.find(REGIONO, k+1)
                if k==-1: raise ValueError('Unmatched '+REGIONA+' in '+pattern)
            tokens.append(pattern[i:k+1]); i=k+1
        elif c == ANYCHAR: tokens.append(ANYCHAR); i+=1
        elif c == ESCAPE:
            if i<pL-1: tokens.append(pattern[i:i+2]); i+=2
            else: raise ValueError('Trailing '+ESCAPE)
        elif nested and c==GROUPA:
            resu = GROUPA; k=i+1; lv=1
            while lv > 0:
                cc = pattern[k]
                if cc == ESCAPE: resu+=cc; resu+=pattern[k+1]; k+=2; continue
                if cc == GROUPA: lv+=1 
                elif cc == GROUPO: lv-=1
                resu+=cc; k+=1
            tokens.append(resu); i=k; kore=strip_groupattris(resu)
            if resu not in TokenListCache.keys():
                TokenListCache[resu] = []   
                # groups are parsed to lists of token lists, each an alternative from '|'
                if kore[0] != GROUPA:
                    for s in kore.split(ALTERNATIVE):
                        TokenListCache[resu].append(parse_pattern(s, True))
                else:
                    TokenListCache[resu].append(parse_pattern(kore, True))
        else: tokens.append(c); i+=1
        if i<pL:
            if pattern[i]==PERHAPS: tokens[-1]=(tokens[-1],PERHAPS); i+=1
            elif pattern[i]==STAR: tokens[-1]=(tokens[-1],STAR); i+=1
            elif pattern[i]==JUST_ONE_and_STAR: 
                tokens.append((tokens[-1],STAR)); tokens[-2]=(tokens[-2],None); i+=1
            else: tokens[-1] = (tokens[-1],None)
        else: tokens[-1] = (tokens[-1],None) 
    TokenListCache[pattern]=tokens; return tokens

def try_index(sarg, tokens, ns):
    tkL=len(tokens)-1; L=len(sarg); global MATCHEND; compix=MATCHEND
    for tix in range(tkL+1):
        if compix==L: return any([pair[1] for pair in tokens[tix:]])
        ctk, qua = tokens[tix]   
        if qua and tix<tkL and try_index(sarg, tokens[tix+1:], ns): return True
        if ns and ctk[0] == GROUPA:
            if any([try_index(sarg, t, True) for t in TokenListCache[ctk]]):
                if ctk[1:3] != SKIPSTORE: xGroups.append(sarg[compix:MATCHEND])
                if ctk.startswith(EXTENSION+'='): continue
                elif ctk.startswith(EXTENSION+'!'): return False
                compix=MATCHEND
                if qua==STAR:
                    T = TokenListCache[ctk]
                    while compix<L:
                        if tix<tkL and try_index(sarg, tokens[tix+1:], ns): return True
                        if not any([try_index(sarg, t, ns) for t in T]): break
                        compix=MATCHEND
            else:
                if ctk.startswith(EXTENSION+'!'): continue
                if tix<tkL or not qua: return False
        elif match_simple_token(sarg, compix, ctk):
            compix+=MATCHLEN; MATCHEND=compix
            if qua==STAR:
                while compix<L:
                    if tix<tkL and try_index(sarg, tokens[tix+1:], ns): return True
                    if not match_simple_token(sarg, compix, ctk): break
                    compix+=MATCHLEN; MATCHEND=compix
        elif tix<tkL or not qua: return False
    return True

def xsearch(sarg, pattern, nested=False, start=0):
    tokens = parse_pattern(pattern, nested); L=len(sarg); global MATCHEND
    if nested: global xGroups; xGroups=[]
    while start<L:
        MATCHEND=start
        if try_index(sarg, tokens, nested): return (start, MATCHEND)
        start+=1
    return ()
    
def xfinditer(sarg, pattern, nested=False, start=0):
    tokens = parse_pattern(pattern, nested); n=0; L=len(sarg); global MATCHEND
    if nested: global xGroups; xGroups=[]
    while start<L:
        if n: start=n
        MATCHEND=start
        if try_index(sarg, tokens, nested): n=MATCHEND; yield (start, MATCHEND)
        else: n=0; start+=1
    raise StopIteration()

def xmatch(sarg, pattern, nested=False):
    """ checks, whether sarg as the whole matches the pattern """
    tokens = parse_pattern(pattern, nested); global MATCHEND; MATCHEND=0
    if nested: global xGroups; xGroups=[]
    if try_index(sarg, tokens, nested) and MATCHEND==len(sarg): return True
    return False

def xsplit(sarg, pattern, nested=False):
    resu = []; xpair = xsearch(sarg, pattern, nested=nested); residue=0
    while xpair:
        resu.append(sarg[:xpair[0]])
        residue = xpair[1]
        xpair = xsearch(sarg, pattern, nested, xpair[1])
    return resu+sarg[residue:]
    
def xreplace(sarg, pattern, subst, nested=False):
    to_replace=[]; s=sarg; xpair=xsearch(sarg, pattern, nested)
    while xpair:
        to_replace.append(xpair); xpair=xsearch(sarg, pattern, nested, xpair[1])
    if nested:
        for i in range(len(xGroups)): subst=subst.replace(ESCAPE+str(i), xGroups[i])
    for xpair in reversed(to_replace): s = s[:xpair[0]]+subst+s[xpair[1]:]   
    return s

def xfuncreplace(sarg, pattern, f, nested=False):
    to_replace=[]; s=sarg; xpair=xsearch(sarg, pattern, nested)
    while xpair:
        to_replace.append(xpair); xpair=xsearch(sarg, pattern, nested, xpair[1])
    for xpair in reversed(to_replace):
        s = s[:xpair[0]]+f(s[xpair[0]:xpair[1]])+s[xpair[1]:]   
    return s
