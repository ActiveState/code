import locale

# Convert a number for human consumption
#
# Divisor can be 1, 1000, 1024
#
# If the locale has been set before this
# function is called, then numbers appropriate to the
# locale will be retured. This is commonly done like:
#     locale.setlocale(locale.LC_ALL,'')
#
# A divisor of 1 => the thousands seperator
# appropriate to ones locale is inserted.
#
# With other divisors the output is aligned
# in a 7 or 8 character column respectively,
# which one can strip() if the display is not
# using a fixed width font.

def number(num, divisor=1, power=""):
    num=float(num)
    if divisor == 1:
        return locale.format("%.f",num,1)
    elif divisor == 1000:
        powers=[" ","K","M","G","T","P"]
    elif divisor == 1024:
        powers=["  ","Ki","Mi","Gi","Ti","Pi"]
    else:
        raise ValueError, "Invalid divisor"
    if not power: power=powers[0]
    while num >= 1000: #4 digits
        num /= divisor
        power=powers[powers.index(power)+1]
    if power.strip():
        num = locale.format("%6.1f",num,1)
    else:
        num = locale.format("%4.f  ",num,1)
    return "%s%s" % (num,power)
