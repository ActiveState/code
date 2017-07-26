from collections import deque

def splitby(pred, seq):

    trues = deque()
    falses = deque()
    iseq = iter(seq)
    
    def pull(source, pred, thisval, thisbuf, otherbuf):
        while 1:
            while thisbuf:
                yield thisbuf.popleft()
            newitem = next(source)
            # uncomment next line to show that source is processed only once
            # print "pulled", newitem
            if pred(newitem) == thisval:
                yield newitem
            else:
                otherbuf.append(newitem)

    true_iter = pull(iseq, pred, True, trues, falses)
    false_iter = pull(iseq, pred, False, falses, trues)
    return true_iter, false_iter
