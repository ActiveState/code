def invert(d):
    return dict( (v,k) for k in d for v in d[k] )
