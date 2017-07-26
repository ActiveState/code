import random
from itertools import izip, imap
from math import log

digits = 4
trials = 100
fmt = '%0' + str(digits) + 'd'
searchspace = tuple([tuple(map(int,fmt % i)) for i in range(0,10**digits)])

def compare(a, b, imap=imap, sum=sum, izip=izip, min=min):
    count1 = [0] * 10
    count2 = [0] * 10
    strikes = 0
    for dig1, dig2 in izip(a,b):
        if dig1 == dig2:
            strikes += 1
        count1[dig1] += 1
        count2[dig2] += 1
    balls = sum(imap(min, count1, count2)) - strikes
    return (strikes, balls)

def rungame(target, strategy, verbose=True, maxtries=15):
    possibles = list(searchspace)
    for i in xrange(maxtries):
        g = strategy(i, possibles)
        if verbose:
            print "Out of %7d possibilities.  I'll guess %r" % (len(possibles), g),
        score = compare(g, target)
        if verbose:
            print ' ---> ', score
        if score[0] == digits:
            if verbose:
                print "That's it.  After %d tries, I won." % (i+1,)
            break
        possibles = [n for n in possibles if compare(g, n) == score]
    return i+1

############################################### Strategy support

def info(seqn):
    bits = 0
    s = float(sum(seqn))
    for i in seqn:
        p = i / s
        bits -= p * log(p, 2)
    return bits

def utility(play, possibles):
    b = {}
    for poss in possibles:
        score = compare(play, poss)
        b[score] = b.get(score, 0) + 1
    return info(b.values())

def hasdup(play, set=set, digits=digits):
    return len(set(play)) != digits

def nodup(play, set=set, digits=digits):
    return len(set(play)) == digits

################################################ Strategies

def s_allrand(i, possibles):
    return random.choice(possibles)

def s_trynodup(i, possibles):
    for j in xrange(20):
        g = random.choice(possibles)
        if nodup(g):
            break
    return g

def s_bestinfo(i, possibles):
    if i == 0:
        return s_trynodup(i, possibles)
    plays = random.sample(possibles, min(20, len(possibles)))
    _, play = max([(utility(play, possibles), play) for play in plays])
    return play

def s_worstinfo(i, possibles):
    if i == 0:
        return s_trynodup(i, possibles)
    plays = random.sample(possibles, min(20, len(possibles)))
    _, play = min([(utility(play, possibles), play) for play in plays])
    return play

def s_samplebest(i, possibles):
    if i == 0:
        return s_trynodup(i, possibles)
    if len(possibles) > 150:
        possibles = random.sample(possibles, 150)
        plays = possibles[:20]
    elif len(possibles) > 20:
        plays = random.sample(possibles, 20)
    else:
        plays = possibles
    _, play = max([(utility(play, possibles), play) for play in plays])
    return play

## Evaluate Strategies

def average(seqn):
    return sum(seqn) / float(len(seqn))

def counts(seqn):
    limit = max(10, max(seqn)) + 1
    tally = [0] * limit
    for i in seqn:
        tally[i] += 1
    return tuple(tally[1:])

from time import clock
print '-' * 60

##for ss in searchspace, filter(hasdup, searchspace), filter(nodup, searchspace):
##    print 'spacesize:', len(ss), ' = ', log(len(ss),2), 'bits'
##for play in [(1,2,3,4,5), (1,1,2,3,4), (1,1,1,2,3), (1,1,2,2,3), (1,1,1,2,2)]:
##    print 'First play:', play, 'has info content', utility(play, searchspace)
##    print 'First play:', play, 'has info content', utility(play, filter(hasdup, searchspace)), 'against dups'
##    print 'First play:', play, 'has info content', utility(play, filter(nodup, searchspace)), 'against nodups'
##    print

for strategy in (s_bestinfo, s_samplebest, s_worstinfo, s_allrand, s_trynodup, s_bestinfo):
    start = clock()
    data = [rungame(random.choice(searchspace), strategy, verbose=False) for i in xrange(trials)]
    #print '[%d  %d| median %.2f    mean %.2f |%d %d]  dig=%d  n=%d   %s' % (min(data), lq(data), median(data),average(data), uq(data), max(data), digits, len(data), strategy.__name__)
    print 'mean=%.2f %r  %s n=%d dig=%d' % (average(data), counts(data), strategy.__name__, len(data), digits)
    print 'Time elapsed %.2f' % (clock() - start,)

""" Analysis of strategies with four digit targets

s_worstinfo             [3 | median 7.00       mean 6.76 | 10]  n=120
s_allrand               [3 | median 6.00       mean 6.19 | 9]  n=120
s_firstnodup            [3 | median 6.00       mean 6.24 | 9]  n=120
s_trynodup              [3 | median 6.00       mean 5.99 | 9]  n=120
s_bestinfo              [2 | median 6.00       mean 5.75 | 10]  n=120

s_worstinfo             [3 | median 7.00       mean 6.86 | 10]  n=200
s_allrand               [4 | median 6.00       mean 6.52 | 10]  n=200
s_firstnodup            [1 | median 6.00       mean 6.19 | 10]  n=200
s_firstdup_restnodup    [3 | median 6.00       mean 6.13 | 10]  n=200
s_trynodup              [3 | median 6.00       mean 6.11 | 10]  n=200
s_bestinfo              [2 | median 6.00       mean 5.73 | 9]  n=200

[3  6| median 7.00    mean 6.78 |8 11]  dig=4  n=200   s_worstinfo            6.77
[3  5| median 6.00    mean 6.24 |7 10]  dig=4  n=200   s_allrand              6.38
[2  6| median 6.00    mean 6.26 |7 9]   dig=4  n=200   s_firstnodup             6.22
[2  5| median 6.00    mean 5.93 |7 9]   dig=4  n=200   s_firstdup_restnodup   6.03
[4  5| median 6.00    mean 6.14 |7 9]   dig=4  n=200   s_trynodup           6.12
[3  5| median 6.00    mean 5.87 |6 9]   dig=4  n=200   s_bestinfo       5.74

[1  6| median 7.00    mean 6.93 |8 11]  dig=4  n=500   s_worstinfo
[2  5| median 6.00    mean 6.11 |7 10]  dig=4  n=500   s_allrand
[3  5| median 6.00    mean 6.12 |7 10]  dig=4  n=500   s_firstnodup
[2  5| median 6.00    mean 6.07 |7 10]  dig=4  n=500   s_firstdup_restnodup
[2  5| median 6.00    mean 6.03 |7 9]  dig=4  n=500   s_trynodup
[2  5| median 6.00    mean 5.82 |6 9]  dig=4  n=500   s_bestinfo
[2  5| median 6.00    mean 5.82 |6 9]  dig=4  n=500   s_bestinfo_randfirst

spacesize: 100000  =  16.6096404744 bits
spacesize: 69760  =  16.0901124197 bits
spacesize: 30240  =  14.8841705191 bits

First play: (1, 2, 3, 4, 5) has info content 2.72731327592
First play: (1, 2, 3, 4, 5) has info content 2.54363363003 against dups
First play: (1, 2, 3, 4, 5) has info content 2.77115216576 against nodups

First play: (1, 1, 2, 3, 4) has info content 2.57287940403
First play: (1, 1, 2, 3, 4) has info content 2.51059435464 against dups
First play: (1, 1, 2, 3, 4) has info content 2.56508152257 against nodups

First play: (1, 1, 1, 2, 3) has info content 2.16683284403
First play: (1, 1, 1, 2, 3) has info content 2.11526590293 against dups
First play: (1, 1, 1, 2, 3) has info content 2.13291456398 against nodups

First play: (1, 1, 2, 2, 3) has info content 2.28656723529
First play: (1, 1, 2, 2, 3) has info content 2.28606417747 against dups
First play: (1, 1, 2, 2, 3) has info content 2.14424289741 against nodups

First play: (1, 1, 1, 2, 2) has info content 2.16683284403
First play: (1, 1, 1, 2, 2) has info content 2.11526590293 against dups
First play: (1, 1, 1, 2, 2) has info content 2.13291456398 against nodups

mean=6.22 (0, 0, 0, 4, 33, 130, 72, 9, 2, 0)  s_samplebest n=250 dig=5
Time elapsed 1395.75

"""
