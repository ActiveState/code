def eight_queens():
    """
    The famous 8Queens problem!
    """
    repetitions = 100

    best_val = min_val
    best_conf = None
    for i in range(repetitions):
        A = generate_configuration()
        b_A = hill_climbing(A)
        v_b_A = value(b_A)
        if value(b_A)< best_val:
            best_val = v_b_A
            best_conf=b_A

    return best_conf

def sons(A):
    """
    The sons of the configuration A for an 8Queen problem
    is obtained reducing properly the space of the solutions.
    In particular, the son is obtained changing the row index of
    one of the queen. In total we have seven possible movement 
    among the column, therefore the number of sons will be 7x8=56.
    """

    tmp_A = list(A)
    N = len(A)
    for i in range(N):
        for r in range(7):
            tmp_A = list(tmp_A)
            q = tmp_A.pop(i)
            tmp_A.insert(i, ((q[0]+1)%7, q[1]) )

            yield tmp_A

    raise StopIteration

def value(A):
    """
    The heuristic for the 8Queen problem is this:
    h(A) = number of attack that the queens have between each
    other.
    The data structure representation for the chessboard
    will be a list of tuples each of them representing the
    coordinates of a the position of a queen.

    Complexity: O(N^2)
    """
    N = len(A)
    h=0
    for i in range(N-1):
        for j in range(i+1, N):
            q1 = A[i]
            q2 = A[j]
            if q1[0] == q2[0]:
                h+=1
            elif q1[1] == q2[1]:
                h+=1
            elif q1[0]+q1[1] == q2[0]+q2[1]:
                h+=1
            elif q1[0]-q1[1] == q2[0]-q2[1]:
                h+=1

    return h

def hill_climbing(A):
    """
    A represents a configuration of the problem.
    It has to be passed as argument of the function sons(A)
    ans value(A) that determines, respectively, the next
    configuration starting from A where Hill Climbing Algorithm
    needs to restart to evaluate and the heuristic function h.

    This function represents a template method.
    """
    best_val = sys.sizemax
    best_conf = None
    for conf in sons(A):
        val = value(conf)
        if best_val > val:
            best_conf = conf
            best_val = val

    if best_conf > value(A):
        return A

    return hill_climbing(best_conf)
