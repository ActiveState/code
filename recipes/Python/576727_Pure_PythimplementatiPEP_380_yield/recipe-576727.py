from compat.functools import wraps as _wraps
from sys import exc_info as _exc_info

class _from(object):
    def __init__(self, EXPR):
        self.iterator = iter(EXPR)

def supergenerator(genfunct):
    """Implements PEP 380. Use as:

        @supergenerator
        def genfunct(*args):
            try:
                sent1 = (yield val1)
                ,,,
                retval = yield _from(iterator)
                ...
            except Exception, e:
                # caller did generator.throw
                pass
            finally:
                pass             # closing
    """

    @_wraps(genfunct)
    def wrapper(*args, **kwargs):
        gen = genfunct(*args, **kwargs)

        try:

            # if first poll of gen raises StopIteration
            # or any other Exception, we propagate
            item = gen.next()

            # OUTER loop
            while True:

                # yield _from(EXPR)
                # semantics based on PEP 380, Revised**12, 19 April
                if isinstance(item, _from):
                    _i = item.iterator
                    try:
                        # first poll of the subiterator
                        _y = _i.next()
                    except StopIteration, _e:
                        # subiterator exhausted on first poll
                        # extract return value
                        _r = _e.args if _e.args else (None,)
                    else:

                        # INNER loop
                        while True:
                            try:
                                # yield what the subiterator did
                                _s = (yield _y)

                            except GeneratorExit, _e:
                                # close the subiterator if possible
                                try:
                                    _close = _i.close
                                except AttributeError:
                                    pass
                                else:
                                    _close()
                                # finally clause will gen.close()
                                raise _e

                            except BaseException:
                                # caller did wrapper.throw
                                _x = _exc_info()
                                # throw to the subiterator if possible
                                try:
                                    _throw = _i.throw
                                except AttributeError:
                                    # doesn't attempt to close _i?
                                    # if gen raises StopIteration
                                    # or any other Exception, we propagate
                                    item = gen.throw(*_x)
                                    _r = None
                                    # fall through to INTERSECTION A
                                    # then to OUTER loop
                                    pass
                                else:
                                    try:
                                        _y = _throw(*_x)
                                    except StopIteration, _e:
                                        _r = _e.args if _e.args else (None,)
                                        # fall through to INTERSECTION A
                                        # then to INTERSECTION B
                                        pass
                                    else:
                                        # restart INNER loop
                                        continue

                                # INTERSECTION A
                                # restart OUTER loop or proceed to B?
                                if _r is None: break

                            else:
                                try:
                                    # re-poll the subiterator
                                    if _s is None:
                                        _y = _i.next()
                                    else:
                                        _y = _i.send(_s)
                                except StopIteration, _e:
                                    # subiterator is exhausted
                                    # extract return value
                                    _r = _e.args if _e.args else (None,)
                                    # fall through to INTERSECTION B
                                    pass
                                else:
                                    # restart INNER loop
                                    continue

                            # INTERSECTION B
                            # done yielding from subiterator
                            # send retvalue to gen

                            # if gen raises StopIteration
                            # or any other Exception, we propagate
                            item = gen.send(_r[0])

                            # restart OUTER loop
                            break

                # traditional yield from gen
                else:
                    try:
                        sent = (yield item)
                    except Exception:
                        # caller did wrapper.throw
                        _x = _exc_info()
                        # if gen raises StopIteration
                        # or any other Exception, we propagate
                        item = gen.throw(*_x)
                    else:
                        # if gen raises StopIteration
                        # or any other Exception, we propagate
                        item = gen.send(sent)

                # end of OUTER loop, restart it
                pass

        finally:
            # gen raised Exception
            # or caller did wrapper.close()
            # or wrapper was garbage collected
            gen.close()

    return wrapper
