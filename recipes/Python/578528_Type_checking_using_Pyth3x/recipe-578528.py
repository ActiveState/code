#!/usr/bin/env python3
"A decorator to use Python3 annotations to type-check inputs and outputs"
import functools

def typecheck(f):
    @functools.wraps(f)
    def decorated(*args, **kws):
        for i, name in enumerate(f.__code__.co_varnames):
            argtype = f.__annotations__.get(name)
            # Only check if annotation exists and it is as a type
            if isinstance(argtype, type):
                # First len(args) are positional, after that keywords
                if i < len(args):
                    assert isinstance(args[i], argtype)
                elif name in kws:
                    assert isinstance(kws[name], argtype)
        result = f(*args, **kws)
        returntype = f.__annotations__.get('return')
        if isinstance(returntype, type):
            assert isinstance(result, returntype)
        return result
    return decorated

#################################
# Simple self-test and examples
#################################

def check(func, TESTS):
    for test in TESTS:
        try:
            args = test[:-1]
            expectation = test[-1]
            print("TEST: %s%r -> float ... " % (func.__name__, args), end="")
            result = func(*args)
            if expectation == "SUCCEED":
                print("Succeed as expected")
            else:
                print("Succeed incorrectly")
        except AssertionError:
            if expectation == "FAIL":
                print("Failed as expected")
            else:
                print("Failed incorrectly")

if __name__ == "__main__":
    @typecheck
    def happy1(a:int, b:list, c:tuple=(1,2,3)) -> float:
        return 3.14

    @typecheck
    def happy_with_nontype(a:int, b:list, x:"non-type", c:tuple=(1,2,3)) -> float:
        return 3.14

    @typecheck
    def happy_wo_annotation(a:int, b, c:tuple=(1,2,3)) -> float:
        return 3.14

    @typecheck
    def unhappy1(a:int, b:str) -> float:
        return 314  # This can never succeed in return type

    check(happy1, [
        (17, ['a','b'], "SUCCEED"),
        (17, ['a','b'], (4,5,6), "SUCCEED"),
        (17.0, ['a','b'], (4,5,6), "FAIL"),
        (17, ('a','b'), "FAIL")])

    check(happy_with_nontype, [
        (17, ['a','b'], "whatever", "SUCCEED"),
        (17, ['a','b'], 0xDEADBEAF, (4,5,6), "SUCCEED"),
        (17.0, ['a','b'], "whatever", (4,5,6), "FAIL"),
        (17, ('a','b'), "whatever", "FAIL")])

    check(happy_wo_annotation, [
        (17, 'b', "SUCCEED"),
        (17, ['a','b'], (4,5,6), "SUCCEED"),
        (17.0, 'b', (4,5,6), "FAIL"),
        (17, 'b', [4,5,6], "FAIL")])

    check(unhappy1, [
        (17, "x", 'FAIL'),
        (1.7, "x", 'FAIL')])
