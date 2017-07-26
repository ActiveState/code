"""
    @author    Thomas Lehmann
    @file      Main.py
    @brief     correlation and regression analyse

    Referring to document at (german):
    http://www.faes.de/Basis/Basis-Statistik/Basis-Statistik-Korrelation-Re/basis-statistik-korrelation-re.html
"""
import sys
import math

EPSILON = 0.0000001

class SimpleLinearRegression:
    """ tool class as help for calculating a linear function """
    def __init__(self, data):
        """ initializes members with defaults """
        self.data = data   # list of (x,y) pairs
        self.a    = 0      # "a" of y = a + b*x
        self.b    = 0      # "b" of y = a + b*x
        self.r    = 0      # coefficient of correlation

    def run(self):
        """ calculates coefficient of correlation and
            the parameters for the linear function """
        sumX, sumY, sumXY, sumXX, sumYY = 0, 0, 0, 0, 0
        n = float(len(self.data))

        for x, y in self.data:
            sumX  += x
            sumY  += y
            sumXY += x*y
            sumXX += x*x
            sumYY += y*y

        denominator = math.sqrt((sumXX - 1/n * sumX**2)*(sumYY - 1/n * sumY**2))
        if denominator < EPSILON:
            return False

        # coefficient of correlation
        self.r  = (sumXY - 1/n * sumX * sumY)
        self.r /= denominator

        # is there no relationship between 'x' and 'y'?
        if abs(self.r) < EPSILON:
            return False

        # calculating 'a' and 'b' of y = a + b*x
        self.b  = sumXY - sumX * sumY / n
        self.b /= (sumXX - sumX**2 / n)

        self.a  = sumY - self.b * sumX
        self.a /= n
        return True

    def function(self, x):
        """ linear function (be aware of current
            coefficient of correlation """
        return self.a + self.b * x

    def __repr__(self):
        """ current linear function for print """
        return "y = f(x) = %(a)f + %(b)f*x" % self.__dict__

def example():
    """ provides an example with error rates (one per session)
        @note linear function verified in open office calc """
    print("Simple linear regression v0.3 by Thomas Lehmann 2012")
    print("...Python %s" % sys.version.replace("\n", ""))
    data   = [(1.0, 18.0), (2, 15.0), (3, 19.0), (4, 10.0)]

    print("...data is %s" % data)

    linRegr = SimpleLinearRegression(data)
    if not linRegr.run():
        print("...error: failed to calculate parameters")
        return

    print("...the coefficient of correlation r = %f (r**2 is %f)" % (linRegr.r, linRegr.r**2))
    print("...parameter a of y = f(x) = a + b*x is %f" % linRegr.a)
    print("...parameter b of y = f(x) = a + b*x is %f" % linRegr.b)
    print("...linear function is then %s" % linRegr)
    print("...forecast of next value: f(5) = %f" % linRegr.function(5))

    firstY = linRegr.function(1)
    lastY  = linRegr.function(4)
    change = (lastY - firstY) / firstY * 100.0

    # keep in mind: reducing of error rate (inverse valuation)!
    if change < 0:
        print("...the trend is about %.1f%% improvement" % -change)
    else:
        print("...the trend is about %.1f%% to the worse" % change)

if __name__ == "__main__":
    example()
