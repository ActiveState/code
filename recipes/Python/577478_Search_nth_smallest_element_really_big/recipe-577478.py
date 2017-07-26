import os
import random
from array import array


def get_sampling_params(filename):
    '''redefine to fit data'''
    filesize = os.path.getsize(filename)

    num_of_chunks = 500
    size_of_chunk = filesize/(100*num_of_chunks)
    seek_positions = [random.randint(0,(filesize-size_of_chunk)) for i
                            in xrange(num_of_chunks)]
    epsilon = 2

    return seek_positions, size_of_chunk, epsilon



def sample_chunks_gen(filename, seek_positions, size_of_chunk):
    '''yields array of floats'''
    def _array_from_file_chunk(input_file, seek_position, size_of_chunk):
        input_file.seek(seek_position)
        buf_str = input_file.read(size_of_chunk)
        first_endl = buf_str.find('\n')
        last_endl = buf_str.rfind('\n')
        return array('f', map(float,
                    buf_str[(first_endl+1):][:(last_endl+1)].splitlines()))

    with open(filename, 'rb') as input_file:
        for seek_position in seek_positions:
            yield _array_from_file_chunk(input_file, seek_position,
                                        size_of_chunk)


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


def get_interval_endpoints(data, position, epsilon):
    '''return interval endpoints'''
    values = select(data, [position-epsilon, position+epsilon])
    return min(values), max(values)


def reduce_endpoints(endpoints):
    '''return min and max of all endpoints'''
    first_endpoint = min(endpoints, key=lambda x: x[0])
    last_endpoint = max(endpoints, key=lambda x: x[1])
    return first_endpoint[0], last_endpoint[1]


def fill_interval(filename, endpoints, size_of_chunk=64*1024):
    '''return count of values before interval, interval, data len'''
    with open(filename, 'rb') as input_file:
        first_endpoint = endpoints[0]
        last_endpoint = endpoints[1]
        seek_position = 0
        interval = array('f')
        iappend = interval.append
        pre_count = 0
        count = 0
        input_file.seek(seek_position)
        buf_str = input_file.read(size_of_chunk)
        while buf_str:
            last_endl = buf_str.rfind('\n')
            buf_arr = array('f', map(float,
                                     buf_str[:(last_endl+1)].splitlines()))
            count = count + len(buf_arr)
            for value in buf_arr:
                if value <= first_endpoint:
                    pre_count = pre_count + 1
                elif last_endpoint <= value:
                    pass
                else:
                    iappend(value)
            seek_position = seek_position + (last_endl+1)
            input_file.seek(seek_position)
            buf_str = input_file.read(size_of_chunk)

    return interval, count, pre_count


def find_value(filename, position, sampling_func=get_sampling_params):
    '''find value in file'''
    seek_positions, size_of_chunk, epsilon = sampling_func(filename)
    s_chunks_iter = sample_chunks_gen(filename, seek_positions, size_of_chunk)
    s_endpoints = map(lambda x:
                            get_interval_endpoints(x, position, epsilon),
                            s_chunks_iter)
    endpoints = reduce_endpoints(s_endpoints)
    interval, count, pre_count = fill_interval(filename, endpoints)
    print len(interval)
    results = select(interval, [position - pre_count])
    return results[0]


if __name__ == '__main__':
    import optparse
    parser = optparse.OptionParser()
    parser.add_option(
        '-f','--file',
        dest='filename',
    )
    parser.add_option(
        '-p','--position',
        dest='position',
        type='int'
    )
    options, args = parser.parse_args()
    print repr(find_value(options.filename, options.position))
