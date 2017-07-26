def sort_by_attr(seq, attr):
    """Sort the sequence of objects by object's attribute

    Arguments:
    seq  - the list or any sequence (including immutable one) of objects to sort.
    attr - the name of attribute to sort by

    Returns:
    the sorted list of objects.
    """
    import operator

    # Use the "Schwartzian transform"
    # Create the auxiliary list of tuples where every i-th tuple has form
    # (seq[i].attr, i, seq[i]) and sort it. The second item of tuple is needed not
    # only to provide stable sorting, but mainly to eliminate comparison of objects
    # (which can be expensive or prohibited) in case of equal attribute values.
    intermed = map(None, map(getattr, seq, (attr,)*len(seq)), xrange(len(seq)), seq)
    intermed.sort()
    return map(operator.getitem, intermed, (-1,) * len(intermed))

def sort_by_attr_inplace(lst, attr):
    """Inplace sort the list of objects by object's attribute
    """
    lst[:] = sort_by_attr(lst, attr)
