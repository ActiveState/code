class CaselessDict(dict):
    """
    A dictionary that isn't case sensitive, and only uses strings as keys.
    Values retain their case.
    """
    # Implementation Omitted

    # A list of keys that must appear first in sorted_keys and sorted_items;
    # must be uppercase.
    canonical_order = None

    def sorted_keys(self):
        """
        Sorts keys according to the canonical_order for the derived class.
        """
        return canonsort_keys(self.keys(), self.canonical_order)

    def sorted_items(self):
        """
        Sorts items according to the canonical_order for the derived class.
        """
        return canonsort_items(self, self.canonical_order)

def canonsort_keys(keys, canonical_order=None):
    """
    Sorts leading keys according to canonical_order.
    Keys not specified in canonical_order will appear alphabetically at the end.

    >>> keys = ['DTEND', 'DTSTAMP', 'DTSTART', 'UID', 'SUMMARY', 'LOCATION']
    >>> canonsort_keys(keys)
    ['DTEND', 'DTSTAMP', 'DTSTART', 'LOCATION', 'SUMMARY', 'UID']
    >>> canonsort_keys(keys, ('SUMMARY', 'DTSTART', 'DTEND', ))
    ['SUMMARY', 'DTSTART', 'DTEND', 'DTSTAMP', 'LOCATION', 'UID']
    >>> canonsort_keys(keys, ('UID', 'DTSTART', 'DTEND', ))
    ['UID', 'DTSTART', 'DTEND', 'DTSTAMP', 'LOCATION', 'SUMMARY']
    >>> canonsort_keys(keys, ('UID', 'DTSTART', 'DTEND', 'RRULE', 'EXDATE'))
    ['UID', 'DTSTART', 'DTEND', 'DTSTAMP', 'LOCATION', 'SUMMARY']
    """
    canonical_map = dict((k, i) for i, k in enumerate(canonical_order or []))
    head = [k for k in keys if k in canonical_map]
    tail = [k for k in keys if k not in canonical_map]
    return sorted(head, key=lambda k: canonical_map[k])  +  sorted(tail)

def canonsort_items(dict1, canonical_order=None):
    """
    Returns a list of items from dict1, sorted by canonical_order.

    >>> d = dict(i=7, c='at', a=3.5, l=(2,3), e=[4,5], n=13, d={'x': 'y'}, r=1.0)
    >>> canonsort_items(d)
    [('a', 3.5), ('c', 'at'), ('d', {'x': 'y'}), ('e', [4, 5]), ('i', 7), ('l', (2, 3)), ('n', 13), ('r', 1.0)]
    >>> canonsort_items(d, ('i', 'c', 'a'))
    [('i', 7), ('c', 'at'), ('a', 3.5), ('d', {'x': 'y'}), ('e', [4, 5]), ('l', (2, 3)), ('n', 13), ('r', 1.0)]
    """
    return [(k, dict1[k]) for k in canonsort_keys(dict1.keys(), canonical_order)]
