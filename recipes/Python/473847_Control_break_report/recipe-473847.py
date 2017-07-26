"""
title        control-break example
author       Ernesto P. Adorio
description  Control break implementation example using finite state machine.
             Actual report formatting to be provided by Python programmer.
"""

# control-break example on branch and salesman sample records.
records = [("branch1",  "sales1", 100),
           ("branch1",  "sales1", 50),
           ("branch1",  "sales2", 10),
           ("branch2",  "sales1", 104),
           ("branch2",  "sales2", 56),
           ("branch2",  "sales2", 156)]

totrecords = len(records)
maxlevels  = 3  # 2 (counting branch and salesman) + 1
EOF        = False

nrecord    = 0
total      = [0] * (maxlevels+1)
oldfields  = [0] * (maxlevels) 
newfields  = [0] * (maxlevels)


def getrecord():
    """
    Rewrite this for specific applications. Must set EOF to True
    if there are no more records.
    """
    global nrecord, totrecords, EOF
    
    nrecord = nrecord + 1
    if nrecord > totrecords:
        EOF = True
        return ()
    return records[nrecord-1]

def header(level):
    print
    print "\t" * level,
    if (level == 0) :
        print "Header Company reports."
    elif level == 1:
        print "Header Branch ", oldfields[level-1] 
    elif level == 2:
        print "Header Salesman ", oldfields[level-1]

def footer(level):
    global total

    print "\t" * level,
    if level == 0:
        print "Footer Company total ", total[level]
    elif level == 1:
        print "Footer Branch total ",  total[level]
    elif level == 2:
        print "Footer Salesman total", total[level]
    print

def detail(level, record, total):
    # Detail line. Shows records and arrays of totals.
    print "\t" * level, record, "total = ", total


# Finite state machine.
def state1(level):
    global total, oldfields, newfields, maxlevels

    if level == maxlevels:
        total[level] = newfields[2]
        detail(level, newfields, total)
        oldfields    = newfields
        newfields    = getrecord()        
        level        = level -1
        state3(level)
    else:
        total[level] = 0
        oldfields     = newfields
        header(level)
        state2(level)

def state2(level):
    global oldfields, newfields
    
    if (not EOF):
        # Compare record fields.
        if oldfields[0:level] != newfields[0:level]:
            state4(level)
        else:
            level += 1
            state1(level)
    else:
        state4(level)

def state3(level):
    global total
    
    total[level] += total[level+1]
    total[level+1] = 0
    state2(level)

def state4(level):
    global total

    footer(level)
    if level > 0:
        level = level - 1
        state3(level)


# Test.
newfields = getrecord()
state1(0)
