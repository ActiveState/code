# mrepalce.py - quick string replacement
import string
import array

def mreplace(s, chararray, newchararray):
    """ Replace occurences of chars in
    chararray in string 's' with elements in
    newchararray """

    slist=list(s)
    dlist=list(chararray)
    rlist=list(newchararray)

    for x in range(0, len(slist)):
        charitem=slist[x]
        if charitem in dlist:
            index=dlist.index(charitem)
            try:
                slist[x]=rlist[index]
            except ValueError:
                pass

    return array.array('c', slist).tostring()
