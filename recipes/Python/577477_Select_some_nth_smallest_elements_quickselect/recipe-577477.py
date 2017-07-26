import random


def select(data, positions, start=0, end=None):
    '''For every n in *positions* find nth rank ordered element in *data*
        inplace select'''
    if not end: end = len(data) - 1
    if end < start:
        return []
    if end == start:
        return [data[start]]
    pivot_rand_i = random.randrange(start,end)
    pivot_rand = data[pivot_rand_i] # get random pivot
    data[end], data[pivot_rand_i] = data[pivot_rand_i], data[end]
    pivot_i = start
    for i in xrange(start, end): # partitioning about the pivot
        if data[i] < pivot_rand:
            data[pivot_i], data[i] = data[i], data[pivot_i]
            pivot_i += 1
    data[end], data[pivot_i] = data[pivot_i], data[end]
    under_positions, over_positions, mid_positions = [],[],[]
    for position in positions:
        if position == pivot_i:
            mid_positions.append(position)
        elif position < pivot_i:
            under_positions.append(position)
        else:
            over_positions.append(position)

    result = []
    if len(under_positions) > 0:
        result.extend(select(data, under_positions, start, pivot_i-1))
    if len(mid_positions) > 0:
        result.extend([data[position] for position in mid_positions])
    if len(over_positions) > 0:
        result.extend(select(data, over_positions, pivot_i+1, end))
    return result
