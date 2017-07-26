"""
Benford's law in Python.
"""

import re
import matplotlib.pyplot as plot

from math import log10

def plot_benford(iterable):
    """Plot leading digit distribution in a string iterable.
    """

    numbers = [float(n) for n in xrange(1, 10)]

    # Plot the frequencies as predicted by the law.
    benford = [log10(1 + 1 / d) for d in numbers]
    plot.plot(numbers, benford, 'ro', label = "Predicted")

    # Plot the actual digit frequencies.
    data = list(digits(iterable))
    plot.hist(data, range(1, 11), align = 'left', normed = True,
              rwidth = 0.7, label = "Actual")

    # Set plot parameters and show it in a window.
    plot.title("Benford's Law")
    plot.xlabel("Digit")
    plot.ylabel("Frequency")

    plot.xlim(0, 10)
    plot.xticks(numbers)
    plot.legend()

    plot.show()

def digits(iterable):
    """Yield leading digits of number-like strings in an iterable.
    """

    numexp = re.compile(r'\d+(\.\d+)?([eE]\d+)?')
    leading = set("123456789")

    for item in iterable:
        for match in numexp.finditer(str(item)):
            for digit in match.group(0):
                if digit in leading:
                    yield int(digit)
                    break

if __name__ == "__main__":
    import fileinput
    plot_benford(fileinput.input())
