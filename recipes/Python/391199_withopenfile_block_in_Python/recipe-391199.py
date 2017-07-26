# Define a "decorator" that, rather than decorating the function,
# calls it, passing it a file object that it had opened as the first
# argument.  Of course, it makes sure to close the file upon the
# function's return (or nonreturn) with a try...finally block. 
# The decorator returns None because we never want to call the
# decorated function ever again; we're using it as a code block.

def call_with_open_file(filename):
    def with_open_file(func):
         flo = open(filename)
         try: func(flo)
         finally: flo.close()
         return None
    return with_open_file


# Example of (ab)use

import sys

@call_with_open_file("readme.txt")
def print_readme(flo):
    for line in flo:
        sys.stdout.write(line)


# print_readme is None afterwards, so we don't accidentlly
# call it again.

assert print_readme is None
