def flatten(lst):
    if lst:
        car,*cdr=lst
        if isinstance(car,(list,tuple)):
            if cdr: return flatten(car) + flatten(cdr)
            return flatten(car)
        if cdr: return [car] + flatten(cdr)
        return [car]
