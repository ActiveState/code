N = 40
[p for p in range(2,N) if 0 not in [p%d for d in range(2,p)]]

# --> [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
