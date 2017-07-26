def DFS (G, v):
    yield v
    visited = set ([v])
    S = neighbors (v)
    while S:
        w = S.pop()
	if w not in visited:
	    yield w
	    visited.add (w)
	    S.extend (neighbors (w))
