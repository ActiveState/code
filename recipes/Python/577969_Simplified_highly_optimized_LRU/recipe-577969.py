def cache_generator(original_function, maxsize):
    mapping = {}
    mapping_get = mapping.get
    root = [None, None]
    root[:] = [root, root]
    value = None
    size = 0

    PREV, NEXT, KEY, VALUE = 0, 1, 2, 3
    while 1:
        key = yield value
        link = mapping_get(key, root)
        if link is root:
            value = original_function(key)
            if size < maxsize:
                size += 1
            else:
                old_prev, old_next, old_key, old_value = root[NEXT]
                root[NEXT] = old_next
                old_next[PREV] = root
                del mapping[old_key]
            last = root[PREV]
            link = [last, root, key, value]
            mapping[key] = last[NEXT] = root[PREV] = link
        else:
            link_prev, link_next, key, value = link
            link_prev[NEXT] = link_next
            link_next[PREV] = link_prev
            last = root[PREV]
            last[NEXT] = root[PREV] = link
            link[PREV] = last
            link[NEXT] = root

def make_cache(original_function, maxsize=100):
    'Create a cache around a function that takes a single argument'
    c = cache_generator(original_function, maxsize)
    next(c)
    return c.send


if __name__ == '__main__':
    p = make_cache(ord, maxsize=3)
    for c in 'abcdecaeaa':
        print(c, p(c))
