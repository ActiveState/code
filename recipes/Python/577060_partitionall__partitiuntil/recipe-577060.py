def partitionall(s, sep=None):
    """
    Search for the separator sep in string s, and return the part before it,
    the separator itself, and the part after it continuously untill all the 
    seperator finishes. If the separator is not found, return string s.
    It works like split() combined with partition()  
    """
    ls = s.split(sep)
    nls = [sep] * (len(ls) * 2 - 1)
    nls[::2] = ls
    return nls

if __name__ == "__main__":
    s = 'This is a, test for, all partition,,'
    sep = ','
    print partitionall(s, sep)
    # result = ['This is a', ',', ' test for', ',', ' all partition', ',', '', ',', '']
