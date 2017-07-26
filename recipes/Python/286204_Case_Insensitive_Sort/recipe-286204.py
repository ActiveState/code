# 06-07-04
#v1.0.0 

# caselesssort.py
# A sort function for lists of strings that is case insensitive.

# Copyright Michael Foord
# You are free to modify, use and relicense this code.

# No warranty express or implied for the accuracy, fitness to purpose or otherwise for this code....
# Use at your own risk !!!

# E-mail michael AT foord DOT me DOT uk
# Maintained at www.voidspace.org.uk/atlantibots/pythonutils.html
    
"""
The built in sort method for lists is case sensitive.
This means it can be unsuitable for sorting some lists of strings.
e.g. ['Apple', 'Pear', 'apple'].sort() 
leaves 'Apple' and 'apple' at opposite ends of the list.

You can pass in a function to the sort method - but this can be very slow.
cSort still uses the sort method, so there isn't much performance hit, but it is caseless.
cSort can handle non-string members in the list without failing.

In addition cSort will sort any sets of entries for which entry1.lower() == entry2.lower()
i.e. cSort(['fish', 'FISH', 'fIsh'])
returns ['FISH', 'fIsh', 'fish']
You can turn this behaviour off by passing cSort an optional 'False' parameter.
 i.e. cSort(['fish', 'FISH', 'fIsh'], False)
returns ['fish', 'FISH', 'fIsh']
"""

def cSort(inlist, minisort=True):
    sortlist = []
    newlist = []
    sortdict = {}
    for entry in inlist:
        try:
            lentry = entry.lower()
        except AttributeError:
            sortlist.append(lentry)
        else:
            try:
                sortdict[lentry].append(entry)
            except KeyError:
                sortdict[lentry] = [entry]
                sortlist.append(lentry)

    sortlist.sort()
    for entry in sortlist:
        try:
            thislist = sortdict[entry]
            if minisort: thislist.sort()
            newlist = newlist + thislist
        except KeyError:
            newlist.append(entry)
    return newlist

if __name__ == '__main__':
    list1 = ['pish', 'fish', 'FISH', 'Fish', 'PISH', 'FIsh', 'fiSH', 'Pish','piSH']
    list2 = list(list1)
    print 'Here is an unsorted list :'
    print list1
    list1.sort()
    print 'Here is a list sorted using list.sort() :'
    print list1
    print 'Here is the list sorted using cSort(list) :'
    print cSort(list2)
    print 'Here is the list sorted using cSort(list, False) :'
    print cSort(list2, False)


"""
TODO/ISSUES


CHANGELOG

06-07-04        Version 1.0.0
A working caseless sort. 
Will be part of the caseless module, but also stands on it's own.

"""
