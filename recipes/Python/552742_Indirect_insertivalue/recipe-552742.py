import random
from exceptions import ValueError


def indirectInsertion(F, ordering, x):
    """
    Inserts x in F array ordered indirectly by ordering.
    """
    L = len(ordering)
    
    #Perform check,
    if L != len(F):
        raise ValueError
    k = L-1
    save = ordering[k] # index to space for x
    
    while k >= 0 and x < F[ordering[k]]:
        ordering[k] = ordering[k-1]
        k -= 1
    k = min(L-1, k+1)
    # print "position to insert x", k
    ordering[k] = save
    F[save] = x
    ordering[k] = save


if __name__  == "__main__":
    #Example.
    #Create random data array.
    F = [random.random() for i in range(10)]

    #Decorate, sort, undecorate
    G = [(f, i) for i, f in enumerate(F)]
    G.sort()
    ordering = [g[1] for g in G]

    print "Original data"
    for i in range(len(F)):
        print i, ordering[i], F[ordering[i]]

    #Generate x to insert indirectly in array F.
    x = random.random()

    print "x to insert=", x
    indirectInsertion(F, ordering, x)
    for i in range(len(F)):
        print i, ordering[i], F[ordering[i]]

When the program runs, it outputs

Original data
0 6 0.0495661645612
1 7 0.0716388504517
2 0 0.181165380138
3 3 0.193601438133
4 8 0.370737951412
5 1 0.409117107263
6 9 0.544771417861
7 5 0.640157511435
8 4 0.831191183469
9 2 0.861514272553
x to insert= 0.463842630209
0 6 0.0495661645612
1 7 0.0716388504517
2 0 0.181165380138
3 3 0.193601438133
4 8 0.370737951412
5 1 0.409117107263
6 2 0.463842630209
7 9 0.544771417861
8 5 0.640157511435
9 4 0.831191183469
