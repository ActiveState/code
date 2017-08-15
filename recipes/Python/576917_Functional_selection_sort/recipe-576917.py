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
    idx, v = min(enumerate(L), key=lambda e: e[1]) # select the minimum
    return [v] + select_sort_r(L[:idx] + L[idx+1:]) # recursively call on the remainder
