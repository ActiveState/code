>>> n = 0
>>> print "%d item%s" % (n, "s"[n==1:])
0 items
>>> n = 1
>>> print "%d item%s" % (n, "s"[n==1:])
1 item
>>> n = 2
>>> print "%d item%s" % (n, "s"[n==1:])
2 items

# If you might want to print negative items, add abs to the test:
>>> n = -1
>>> print "%d item%s" % (n, "s"[abs(n)==1:])
2 items

# If a word has irregular plural morphology, use a list:
>>> n=1
>>> print "%d %s" % (n, ['abacus','abaci'][n!=1])
1 abacus
>>> n=2
>>> print "%d %s" % (n, ['abacus','abaci'][n!=1])
2 abaci
