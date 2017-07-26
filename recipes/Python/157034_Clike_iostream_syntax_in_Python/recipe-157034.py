import sys

class IOManipulator:

    def __init__(self, function=None):
        self.function = function

    def do(self, output):
        self.function(output)


class OStream:

    def __init__(self, output=None):
        if output is None:
            output = sys.stdout
        self.output = output

    def __lshift__(self, thing):
        if isinstance(thing, IOManipulator):
            thing.do(self.output)
        else:
            self.output.write(str(thing))
        return self


def main():
    endl = IOManipulator(lambda s: (s.write('\n'), s.flush()))
    cout = OStream()
    cout << "The average of " << 1 << " and " << 3 << " is " << (1 + 3)/2 << endl

if __name__ == '__main__': main()
