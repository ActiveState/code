import re
from string import zfill
numbers = re.compile('\d+')

def increment(s):
    """ look for the last sequence of number(s) in a string and increment """
    if numbers.findall(s):
        lastoccr_sre = list(numbers.finditer(s))[-1]
        lastoccr = lastoccr_sre.group()
        lastoccr_incr = str(int(lastoccr) + 1)
        if len(lastoccr) > len(lastoccr_incr):
            lastoccr_incr = zfill(lastoccr_incr, len(lastoccr))
        return s[:lastoccr_sre.start()]+lastoccr_incr+s[lastoccr_sre.end():]

    return s

def T(_):
    print "from",_, "to", increment(_)
if __name__=='__main__':
    T("10dsc_0010.jpg")
    T("dsc_9.jpg")
    T("0000001.exe")
    T("ref-04851")
