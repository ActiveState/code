# simplest, no-checks code for sample manipulations of a list
# (but if alist has, e.g., .append and not .extend, *it will
# be partially altered* before an exception is raised...)
def munge1(alist):
    alist.append(23)
    alist.extend(range(5))
    alist.append(42)
    alist[4] = alist[3]
    alist.extend(range(2))

# naive "look before you leap": safer, but loses polymorphism
def munge2(alist):
    if type(alist)==type([]):
        munge1(alist)

# accurate "look before you leap": safer AND fully polymorphic
def munge3(alist):
    # first, we extract all bound-methods we'll need
    append = alist.append
    extend = alist.extend

    # then, we check operations, such as indexing
    try: a[0]=a[0]
    except IndexError: pass    # empty alist's OK

    # and finally, we operate -- no exceptions expected
    append(23)
    extend(range(5))
    append(42)
    alist[4] = alist[3]
    extend(range(2))
