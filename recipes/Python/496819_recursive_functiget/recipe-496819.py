def permu(xs):
    if xs:
        r , h = [],[]
        for x in xs:
            if x not in h:
                ts = xs[:]; ts.remove(x)
                for p in permu(ts):
                    r.append([x]+p)
            h.append(x)
        return r
    else:
        return [[]]

def permu2(xs):
    if len(xs)<2: yield xs
    else:
        h = []
        for x in xs:
            h.append(x)
            if x in h[:-1]: continue
            ts = xs[:]; ts.remove(x)
            for ps in permu2(ts):
                yield [x]+ps


print permu([1,2,3])
print
print list(permu2([4,5,6,6]))
print
print permu(['a',[1,2],'a',[1,2]])

----------- we get --------------------
[[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]

[[4, 5, 6, 6], [4, 6, 5, 6], [4, 6, 6, 5], [5, 4, 6, 6], [5, 6, 4, 6], [5, 6, 6, 4], 
[6, 4, 5, 6], [6, 4, 6, 5], [6, 5, 4, 6], [6, 5, 6, 4], [6, 6, 4, 5], [6, 6, 5, 4]]

[['a', [1, 2], 'a', [1, 2]], ['a', [1, 2], [1, 2], 'a'], ['a', 'a', [1, 2], [1, 2]], 
[[1,2], 'a', 'a', [1, 2]], [[1, 2], 'a', [1, 2], 'a'], [[1, 2], [1, 2], 'a', 'a']]
