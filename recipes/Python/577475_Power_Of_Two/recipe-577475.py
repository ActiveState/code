import time
import cProfile

class Timer:
    # on Windows this is more precise than 'time.time'.
    function = time.clock

    # is providing a start time
    @staticmethod
    def value():
        return Timer.function()

    # calculating delta between current time and start time.
    @staticmethod
    def delta(start):
        return Timer.function() - start

# background information: http://en.wikipedia.org/wiki/Power_of_two
class PowerOfTwo:
    # main calculation
    @staticmethod
    def calculateDigits(digits, n, f):
        maxk = len(digits)-1
        while n > 0:
            rest = 0
            k    = 0
            while k <= maxk:
                digits[k]  = digits[k] * f + rest
                rest       = digits[k] // 10
                digits[k] %= 10
                k += 1

            if rest > 0:
                digits.append(rest)
                maxk += 1

            n -= 1

    # calculating the power of two
    @staticmethod
    def calculate(n):
        digits = [1]

        # little performance improvement
        for k in [3, 2]:
            if n > 2**k:
                PowerOfTwo.calculateDigits(digits, n // k, 2**k)
                n %= k

        if n > 0:
            PowerOfTwo.calculateDigits(digits, n, 2)
        digits.reverse()
        return digits

    @staticmethod
    def dump(digits, digitsPerRow = 50):
        count        = 0
        text         = ""
        for digit in digits:
            if count % digitsPerRow == 0:
                text += "\n"
            text  += "%d" % (digit)
            count += 1
        print(text)

def main():
    n      = 4000
    start  = Timer.value()
    digits = PowerOfTwo.calculate(n)

    print("2^%d:" % (n))
    print("...%d digits calculated" % (len(digits)))
    print("...took %f seconds" % (Timer.delta(start)))

    PowerOfTwo.dump(digits)

if __name__ == "__main__":
    main()
    #cProfile.run("main()")
