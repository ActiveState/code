class Interpolator:
    def __init__(self, name, func, points, deriv=None):
        self.name = name  # used for naming the C function
        self.intervals = intervals = [ ]
        # Generate a cubic spline for each interpolation interval.
        for u, v in map(None, points[:-1], points[1:]):
            FU, FV = func(u), func(v)
            # adjust h as needed, or pass in a derivative function
            if deriv == None:
                h = 0.01
                DU = (func(u + h) - FU) / h
                DV = (func(v + h) - FV) / h
            else:
                DU = deriv(u)
                DV = deriv(v)
            denom = (u - v)**3
            A = ((-DV - DU) * v + (DV + DU) * u +
                 2 * FV - 2 * FU) / denom
            B = -((-DV - 2 * DU) * v**2  +
                  u * ((DU - DV) * v + 3 * FV - 3 * FU) +
                  3 * FV * v - 3 * FU * v +
                  (2 * DV + DU) * u**2) / denom
            C = (- DU * v**3  +
                 u * ((- 2 * DV - DU) * v**2  + 6 * FV * v
                                    - 6 * FU * v) +
                 (DV + 2 * DU) * u**2 * v + DV * u**3) / denom
            D = -(u *(-DU * v**3  - 3 * FU * v**2) +
                  FU * v**3 + u**2 * ((DU - DV) * v**2 + 3 * FV * v) +
                  u**3 * (DV * v - FV)) / denom
            intervals.append((u, A, B, C, D))

    def __call__(self, x):
        def getInterval(x, intervalList):
            # run-time proportional to the log of the length
            # of the interval list
            n = len(intervalList)
            if n < 2:
                return intervalList[0]
            n2 = n / 2
            if x < intervalList[n2][0]:
                return getInterval(x, intervalList[:n2])
            else:
                return getInterval(x, intervalList[n2:])
        # Tree-search the intervals to get coefficients.
        u, A, B, C, D = getInterval(x, self.intervals)
        # Plug coefficients into polynomial.
        return ((A * x + B) * x + C) * x + D

    def c_code(self):
        """Generate C code to efficiently implement this
        interpolator. Run the C code through 'indent' if you
        need it to be legible."""
        def codeChoice(intervalList):
            n = len(intervalList)
            if n < 2:
                return ("A=%.10e;B=%.10e;C=%.10e;D=%.10e;"
                        % intervalList[0][1:])
            n2 = n / 2
            return ("if (x < %.10e) {%s} else {%s}"
                    % (intervalList[n2][0],
                       codeChoice(intervalList[:n2]),
                       codeChoice(intervalList[n2:])))
        return ("double interpolator_%s(double x) {" % self.name +
                "double A,B,C,D;%s" % codeChoice(self.intervals) +
                "return ((A * x + B) * x + C) * x + D;}")
