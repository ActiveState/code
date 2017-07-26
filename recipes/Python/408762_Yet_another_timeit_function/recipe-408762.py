def timeit(*args):
    "Run the timeit.main function with args, catch and parse the output."
    import sys
    import re
    import timeit
    import cStringIO

    prev_stdout = sys.stdout
    sys.stdout = cStringIO.StringIO()

    timeit.main(args)

    out = sys.stdout.getvalue()
    sys.stdout = prev_stdout
    # Parse the output, and apply our own formatting
    match = re.search(r"(\d+\.\d*|\d+) usec", out)
    time = float(match.group(1))
    print "%8.2f us: %s" % (time, args[-1])

if __name__ == "__main__":
    timeit("object()")
    timeit("list()")
    timeit("[]")
    timeit("int()")
    timeit("-s", "rng = range(32)",
           "[i for i in rng]    # a list comp")
    timeit("-s", "class ClassicClass: pass",
           "ClassicClass()      # create a classic class instance")
    timeit("-s", "class NewStyleClass(object): pass",
           "NewStyleClass()     # create a new style class instance")
