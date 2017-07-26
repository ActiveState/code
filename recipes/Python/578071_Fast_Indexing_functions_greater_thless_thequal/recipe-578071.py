def first_index_gt(data_list, value):
    '''return the first index greater than value from a given list like object'''
    try:
        index = next(data[0] for data in enumerate(data_list) if data[1] > value)
        return index
    except StopIteration: return - 1

def first_index_lt(data_list, value):
    '''return the first index less than value from a given list like object'''
    try:
        index = next(data[0] for data in enumerate(data_list) if data[1] < value)
        return index
    except StopIteration: return - 1

def first_index_ne(data_list, value):
    '''returns first index not equal to the value from list'''
    try:
        index = next(data[0] for data in enumerate(data_list) if data[1] != value)
        return index
    except StopIteration: return - 1

def first_index_et(data_list, value):
    '''same as data_list.index(value), except with exception handling
    Also finds 'nan' values'''
    try:
        if type(value) == float and math.isnan(value):
            return next(data[0] for data in enumerate(data_list)
              if (type(data[1]) in (float, np.float64, np.float32, np.float96)
              and math.isnan(data[1])))
        else:
            return next(data[0] for data in enumerate(data_list) if data[1] == value)
    except (ValueError, StopIteration): return - 1
