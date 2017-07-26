import itertools
import collections

def nth(iterable, n, default=None):
    "Returns the nth item or a default value"
    return next(itertools.islice(iterable, n, None), default)

def find(item, source, depth=1, queue_limit=1000000, found_limit=1000000):
    "Tries to find a pathway to access item from source."
    assert depth > 0, 'Cannot find item in source!'
    candidates = collections.deque([(source, 'source', 1)])
    locations = {id(source)}
    while candidates:
        if len(candidates) > queue_limit or len(locations) > found_limit:
            break
        source, path, level = candidates.pop()
        # Search container.
        try:
            iterator = iter(source)
        except TypeError:
            pass
        else:
            for key, value in enumerate(iterator):
                if isinstance(source, dict):
                    key, value = value, source[value]
                addr = id(value)
                if addr not in locations:
                    try:
                        assert source[key] is value
                    except (AssertionError, KeyError, TypeError):
                        attr_path = 'nth({}, {})'.format(path, key)
                    else:
                        attr_path = '{}[{!r}]'.format(path, key)
                    if value is item:
                        return attr_path
                    if level < depth:
                        candidates.appendleft((value, attr_path, level + 1))
                        locations.add(addr)
        # Search attributes.
        for name in dir(source):
            try:
                attr = getattr(source, name)
            except AttributeError:
                pass
            else:
                addr = id(attr)
                if addr not in locations:
                    attr_path = '{}.{}'.format(path, name)
                    if attr is item:
                        return attr_path
                    if level < depth:
                        candidates.appendleft((attr, attr_path, level + 1))
                        locations.add(addr)
