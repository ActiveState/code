def genWhile(g, condition):
    """
    run generator g while 'condition' is true.
    Condition is a partial expression such as "< 10"
    to be evaluated with g.next() as the left side
    """
    while 1:
        next = g.next()
        if eval("next " + condition):
            yield next
        else:
            return


def genEven():
    x = 0
    while 1:
        x += 2
        yield x


def main():
    print [x for x in genWhile(genEven(), "< 12")]
