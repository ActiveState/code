from collections import deque
from bisect import insort

def grouper(seq, n):
    'Split sequence into n-length deques'
    return [deque(seq[i:i+n]) for i in range(0, (len(seq)+n-1)//n*n, n)]


class RunningMedian:
    ''' Updates median value over a sliding window.

    Initialize with a window size of data.  The call update(elem) with
    new values.  Returns the new median (for an odd-sized window).

    '''
    # Gains speed by maintaining a sort while inserting new values
    # and deleting the oldest ones.

    # Reduction of insert/delete time is done by chunking sorted data
    # into subgroups organized as deques, so that appending and popping
    # are cheap.  Running-time per update is proportional to the
    # square-root of the window size.

    # Inspired by "Efficient Algorithm for computing a Running Median"
    # by Soumya D. Mohanty.  Adapted for Python by eliminating the
    # map structure, check structure, and by using deques.

    def __init__(self, iterable):
        self.q = q = deque(iterable)                            # track the order that items are added
        n = int(len(q) ** 0.5)                                  # compute optimal chunk size
        self.chunks = grouper(sorted(q), n)                     # sorted list of sorted n-length subsequences
        row, self.midoffset = divmod((len(q) - 1) // 2, n)      # locate the mid-point (median)
        self.midchunk = self.chunks[row]

    def update(self, new_elem, check_invariants=False):
        # update the main queue that tracks values in the order added
        old_elem = self.q.popleft()
        self.q.append(new_elem)

        # insert new element into appropriate chunk (where new_elem less that rightmost elem in chunk)
        chunks = self.chunks
        for new_index, chunk in enumerate(chunks):
            if new_elem < chunk[-1]:
                break
        data = list(chunk)
        insort(data, new_elem)
        chunk.clear()
        chunk.extend(data)

        # remove oldest element
        for old_index, chunk in enumerate(chunks):
            if old_elem <= chunk[-1]:
                break
        chunk.remove(old_elem)

        # restore the chunk sizes by shifting end elements
        # chunk at new_index is too fat
        # chunk at old_index is too thin
        if new_index < old_index:
            # propagate the now-too-fat chunk to the right
            for i in range(new_index, old_index):
                chunks[i+1].appendleft(chunks[i].pop())
        elif new_index > old_index:
            # feed the now-too-thin chunk from the right
            for i in range(old_index, new_index):
                chunks[i].append(chunks[i+1].popleft())

        # check-invariants (slow)
        if check_invariants:
            assert sorted(self.q) == [elem for chunk in chunks for elem in chunk]
            assert len(set(map(len, chunks))) <= 2              # are chunk sizes balanced ?

        # return median
        return self.midchunk[self.midoffset]



if __name__ == '__main__':
    from random import randrange
    from itertools import islice

    window_size = 41
    data = [randrange(200) for i in range(1000)]

    it = iter(data)
    r = RunningMedian(islice(it, window_size))
    medians = [r.update(elem, True) for elem in it]

    midpoint = (window_size - 1) // 2
    median = lambda window: sorted(window)[midpoint]
    target_medians = [median(data[i:i+window_size]) for i in range(1, len(data)-window_size+1)]

    assert medians == target_medians
    print(medians)
