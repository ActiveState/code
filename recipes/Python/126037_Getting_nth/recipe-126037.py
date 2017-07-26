def getPerm(seq, index):
    "Returns the <index>th permutation of <seq>"
    seqc= list(seq[:])
    seqn= [seqc.pop()]
    divider= 2 # divider is meant to be len(seqn)+1, just a bit faster
    while seqc:
        index, new_index= index//divider, index%divider
        seqn.insert(new_index, seqc.pop())
        divider+= 1
    return seqn
