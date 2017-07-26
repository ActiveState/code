# bmh.py
#
# An implementation of Boyer-Moore-Horspool string searching.
#
# This code is Public Domain.
#
def BoyerMooreHorspool(pattern, text):
    m = len(pattern)
    n = len(text)
    if m > n: return -1
    skip = []
    for k in range(256): skip.append(m)
    for k in range(m - 1): skip[ord(pattern[k])] = m - k - 1
    skip = tuple(skip)
    k = m - 1
    while k < n:
        j = m - 1; i = k
        while j >= 0 and text[i] == pattern[j]:
            j -= 1; i -= 1
        if j == -1: return i + 1
        k += skip[ord(text[k])]
    return -1

if __name__ == '__main__':
    text = "this is the string to search in"
    pattern = "the"
    s = BoyerMooreHorspool(pattern, text)
    print 'Text:',text
    print 'Pattern:',pattern
    if s > -1:
        print 'Pattern \"' + pattern + '\" found at position',s
