import sys
if sys.version_info >= (3,):
    xrange = range

def rev_range(*args):
    """Create a reversed range.

    Equivalent to reversed(list(range(*args))), but without the intermediate
    list.

    This does some simple math on the arguments instead of creating an
    intermediate list and reversing it, thus automating a simple but
    error-prone optimization.
    """
    # Before Python 3.0, range creates a list while xrange is an efficient
    # iterator. From 3.0 onwards, range does what xrange did earlier (and
    # xrange is gone).
    if len(args) == 1:
        # start = 0, stop = args[0], step = 1
        return xrange(args[0]-1, -1, -1)

    # Unpack arguments, setting 'step' to 1 if it is not given.
    start, stop, step = (args + (1,))[:3]

    # The new 'stop' is the first item of the original range plus/minus one,
    # depending on the step's sign. Specifically:
    #   new_stop = start - (1 if step > 0 else -1)
    #
    # The new 'start' is the last item of the original range, which is
    # between one and 'step' less than the original 'stop'. Specifically:
    #
    # * If 'stop' minus 'start' divides by 'step' then the last item of the
    #   original range is 'stop' minus 'step'.
    # * If 'stop' minus 'start' doesn't divide by 'step', then the last item of
    #   the original range is 'stop' minus the remainder of this division.
    #
    # A single expression which accounts for both cases is:
    #   new_start = stop - ((stop-start-1) % step + 1)
    return xrange(stop - ((stop-start-1) % step + 1),
                  start - (1 if step > 0 else -1),
                  -step)
