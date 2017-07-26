def allperm(inputstr):
    for i in range(len(inputstr)):
        yield(inputstr[i])        
        for s in allperm(inputstr[:i] + inputstr[i+1:]):
            yield(inputstr[i] + s)
