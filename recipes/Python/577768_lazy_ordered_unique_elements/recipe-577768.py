def unique(iterable, key=None):
    seen = set()

    if key is None:
        # Optimize the common case
        for item in iterable:
            if item in seen:
                continue
            seen.add(item)
            yield item

    else:
        for item in iterable:
            keyitem = key(item)
            if keyitem in seen:
                continue
            seen.add(keyitem)
            yield item

if __name__ == "__main__":
    assert list(unique("abcd")) == list("abcd"), (list(unique("abcd")), "abcd".split())
    assert list(unique("abca")) == list("abc")
    assert list(unique("baaca")) == list("bac")
    assert list(unique("")) == []

    assert list(unique("to be or not to be".split())) == "to be or not".split()
    assert list(unique("to be or not to be".split(), key=len)) == "to not".split()

    assert list(unique(set("cabbage"))) == list(unique(set("cabbage")))
    print("All tests passed.")
