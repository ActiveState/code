def sample(n, r):
    "Generate r randomly chosen, sorted integers from [0,n)"
    rand = random.random
    pop = n
    for samp in xrange(r, 0, -1):
        cumprob = 1.0
        x = rand()        
        while x < cumprob:
            cumprob -= cumprob * samp / pop
            pop -= 1
        yield n-pop-1


# Example call to select three samples in range(0,10)
>>> list(sample(10, 3))
[2, 7, 8]
