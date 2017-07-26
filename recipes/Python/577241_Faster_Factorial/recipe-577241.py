_FAC_TABLE = [1, 1]
def factorial(n):
    if n < len(_FAC_TABLE):
        return _FAC_TABLE[n]

    last = len(_FAC_TABLE) - 1
    total = _FAC_TABLE[last]
    for i in range(last + 1, n + 1):
        total *= i
        _FAC_TABLE.append(total)

    return total


def main():
    from timeit import Timer
    print("factorial:      %.5f s" %
            Timer("factorial(500)", "from __main__ import factorial")
            .timeit(1000))

    import math
    if hasattr(math, "factorial"):
        print("math.factorial: %.5f s" %
                Timer("factorial(500)", "from math import factorial")
                .timeit(1000))


if __name__ == "__main__":
    main()
