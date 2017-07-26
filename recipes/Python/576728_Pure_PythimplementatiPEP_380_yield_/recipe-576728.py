from compat.functools import wraps as _wraps
from sys import exc_info as _exc_info

from weakref import WeakValueDictionary as _WeakValueDictionary
# use WeakValueDictionary to associate data with generator instances
# for alternative, wrapper-based solutions, see
# <http://code.activestate.com/recipes/164044/>
_yieldingfrom = _WeakValueDictionary()


class _shared_stack(object):
    """Stack whose top parts can also be stacks.

    Sample usage:

    >>> m = _shared_stack(); m.push("m", [])
    >>> n = _shared_stack(m); m.push("n", [])    # initialize n from m's head
    >>>                                          # m and n now have same head
    >>> o = _shared_stack(n); n.push("o", [])    # pushes to both
    >>> p = _shared_stack(n)
    >>> q = _shared_stack(); n.push("p", q.root())
    >>> m._trace()
    []                              # q's root, head of m,n,o,p,q
    ['p', []]                       # p's root, top of m,n,o,p
    ['o', ['p', []]]
    ['n', ['o', ['p', []]]]         # n's root
    ['m', ['n', ['o', ['p', []]]]]  # m's root
    >>> m._headstack()[0] is q.root()
    True
    """
    def __init__(self, data=None):
        """Initializing with another shared_stack
        makes a stack with the same head."""
        if data is None:
            data = []
        elif isinstance(data, _shared_stack):
            data, _ = data._headstack()
        # Implemented as a dict:
        # {'head': head_list, list_id: previous_list, ...
        #  'root': root_list, root_list_id: True}
        self._stack = {'head': data, 'root': data, id(data): True}

    def _headstack(self):
        stack = self._stack
        head = stack['head']
        while True:
            # pop levels until previous_list is not empty
            head_id = id(head)
            if stack[head_id]:
                # root_list_id also points to a True value
                break
            stack['head'] = head = stack.pop(head_id)
        while head:
            # expand until previous_list's final element is empty
            stack['head'] = next = head[-1]
            stack[id(next)] = head
            head = next
        return head, stack

    def root(self):
        return self._stack['root']

    def top(self):
        head, stack = self._headstack()
        top = stack[id(head)]
        return (top if top is not True else None)

    def push(self, *args):
        head, _ = self._headstack()
        head.extend(args)

    def pop(self):
        head, stack = self._headstack()
        if head is stack['root']:
            raise IndexError("pop from empty stack")
        stack['head'] = prev = stack.pop(id(head))
        del prev[:]

    def __nonzero__(self):
        head, stack = self._headstack()
        return head is not stack['root']

    def _trace(self):
        head, stack = self._headstack()
        print "Tracing 0x%x:" % (id(self),)
        while True:
            print '0x%x=%s' % (id(head), head)
            head = stack[id(head)]
            if head is True: break

    def __repr__(self):
        return '_shared_stack(%r)' % (self._shared_stack['root'],)





class _from(object):
    def __init__(self, EXPR):
        self.iterator = iter(EXPR)

def supergenerator(genfunct):
    """Implements PEP 380. Use as:

        @supergenerator
        def genfunct(*args):
            try:
                sent1 = (yield val1)
                ...
                retval = yield _from(iterator)
                ...
            except Exception, e:
                # caller did generator.throw
                pass
            finally:
                # closing
                pass
    """

    @_wraps(genfunct)
    def wrapper(*args, **kwargs):
        gen = genfunct(*args, **kwargs)
        _yieldingfrom[gen] = gen_yf = _stack()

        try:
            # if first poll of gen raises StopIteration
            # or any other Exception, we propagate
            item = gen.next()

            # OUTER loop
            while True:

                # yield _from(EXPR)
                # semantics based on PEP 380, Revised**12, 19 April
                if isinstance(item, _from):
                    _i, _iyf = item.iterator, None
                    try:
                        # first poll of the subiterator
                        _y = _i.next()
                    except StopIteration, _e:
                        # subiterator exhausted on first poll
                        # extract return value
                        _r = _e.args
                        if not _r: _r = (None,)
                    else:

                        # if subgenerator is another supergenerator
                        # extract the root of its gen_yf shared_stack
                        try:
                            _iyf = _i.gi_frame.f_locals['gen']
                        except (AttributeError,KeyError):
                            _iyf = []
                        else:
                            _iyf = _yieldingfrom.get(_iyf,[])
                            if isinstance(_iyf, _stack):
                                _iyf = _iyf.root()
                        gen_yf.push(_i, _iyf)

                        # INNER loop
                        while True:

                            if _iyf is None:
                                # subiterator was adopted by caller
                                # and is now exhausted
                                item = _y
                                break

                            try:
                                # yield what the subiterator did
                                _s = (yield _y)

                            except GeneratorExit, _e:
                                # close as many subiterators as possible
                                while gen_yf:
                                    _i, _iyf = gen_yf.top()
                                    try:
                                        _close = _i.close
                                    except AttributeError:
                                        pass
                                    else:
                                        _close()
                                    gen_yf.pop()
                                # finally clause will gen.close()
                                raise _e

                            except BaseException:
                                # caller did wrapper.throw
                                _x = _exc_info()
                                # throw to the subiterator if possible
                                while gen_yf:
                                    _i, _iyf = gen_yf.top()
                                    try:
                                        _throw = _i.throw
                                    except AttributeError:
                                        # doesn't attempt to close _i?
                                        # try throwing to subiterator's parent
                                        pass
                                    else:
                                        try:
                                            _y = _throw(*_x)
                                        except StopIteration, _e:
                                            _r = _e.args
                                            if not _r: _r = (None,)
                                            # drop to INTERSECTION A
                                            # then to INTERSECTION B
                                            break
                                        else:
                                            _r = None
                                            # drop to INTERSECTION A
                                            # then to INNER loop
                                            break
                                    gen_yf.pop()
                                else:
                                    # if gen raises StopIteration
                                    # or any other Exception, we propagate
                                    _y = gen.throw(*_x)
                                    _r = _iyf = None
                                    # fall through to INTERSECTION A
                                    # then to INNER loop then to OUTER loop
                                    pass

                                # INTERSECTION A
                                # restart INNER loop or proceed to B?
                                if _r is None: continue

                            # caller did send/next
                            else:
                                if not gen_yf:
                                    # subiterator was adopted by caller
                                    # and is now exhausted
                                    _r = (_s,)
                                    _iyf = None
                                    # fall through to INTERSECTION B
                                    pass
                                else:
                                    if _iyf:
                                        # check if current _i itself
                                        # now yielding from a subiterator?
                                        _i, _iyf = gen_yf.top()
                                    try:
                                        # re-poll the subiterator
                                        if _s is None:
                                            _y = _i.next()
                                        else:
                                            _y = _i.send(_s)
                                    except StopIteration, _e:
                                        # subiterator is exhausted
                                        # extract return value
                                        _r = _e.args
                                        if not _r: _r = (None,)
                                        # fall through to INTERSECTION B
                                        pass
                                    else:
                                        # restart INNER loop
                                        continue

                            # INTERSECTION B
                            # done yielding from active subiterator
                            # send retvalue to its parent

                            while True:
                                if _iyf is not None:
                                    gen_yf.pop()
                                if gen_yf:
                                    _i, _iyf = gen_yf.top()
                                    try:
                                        # push retval to subiterator's parent
                                        _y = _i.send(_r[0])
                                    except StopIteration, _e:
                                        # parent is exhausted, try _its_ parent
                                        _r = _e.args
                                        if not _r: _r = (None,)
                                        continue
                                    else:
                                        # fall through to INTERSECTION C
                                        # then to INNER loop
                                        pass
                                else:
                                    # gen_yf is empty, push return value to gen
                                    # if gen raises StopIteration

                                    # or any other Exception, we propagate
                                    _y = gen.send(_r[0])
                                    _iyf = None
                                    # fall through to INTERSECTION C
                                    # then to INNER loop then to OUTER loop
                                    pass

                                # INTERSECTION C
                                # passed retvalue, continue INNER loop
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
