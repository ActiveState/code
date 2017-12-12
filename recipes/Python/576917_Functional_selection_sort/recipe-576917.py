selection_sort = lambda sort_list: reduce(
    lambda my_list, i: (
        lambda max_value=reduce(
            lambda a, b: b if b > a else a,
            my_list[1]
        ): [
            my_list[1].remove(max_value),
            my_list[0].append(max_value)
        ] and  my_list
    )(),
    range(len(sort_list)),
    [[], sort_list]
)[0]

test_list = [ 5, 1, 7, 0, -3, -10, 10, -6, 1, 0, 2, 4, -2, 6, 5, 8, 2]
print test_list
print selection_sort(test_list)


# Recursive version
def select_sort_r(L):
    if not L: return [] # terminal case 
    v, idx = min((v, i) for i, v in enumerate(L)) # select the smallest
    return [v] + select_sort_r(L[:idx] + L[idx+1:]) # recursively call on the remainder


# Lambda version 
# Python > 2.7.10 and above
select_sort_l = (
    lambda L: [] if not L else (
        lambda idx, v: [v] + select_sort_l(L[:idx] + L[idx + 1:]))(
            *min(enumerate(L), key=lambda t: t[1])
    )
)

# OP's version from the comments, works probably for Python < 2.7.10 
selsort2 = (lambda l: [] if not l else
            (lambda (idx, v): [v] + selsort2(l[:idx] + l[idx + 1:]))
            (min(enumerate(l), key=lambda(i, x): x)))


# OP's original test_list gets mutated by the functional version
test_list = [5, 1, 7, 0, -3, -10, 10, -6, 1, 0, 2, 4, -2, 6, 5, 8, 2]
expected  = [-10, -6, -3, -2, 0, 0, 1, 1, 2, 2, 4, 5, 5, 6, 7, 8, 10]

assert select_sort_r(test_list) == expected 
assert select_sort_l(test_list) == expected 
# assert selsort2(test_list) == expected 
