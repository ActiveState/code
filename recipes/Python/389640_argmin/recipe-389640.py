def argmin(sequence, fn=None):
    """Two usage patterns:
    argmin([s0, s1, ...], fn)
    argmin([(fn(s0), s0), (fn(s1, s1), ...]) 
    Both return the si with lowest fn(si)"""
    if fn is None:
        return min(sequence)[1]
    else:
        return min((fn(e), e) for e in sequence)[1]
