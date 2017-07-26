def getNum(n):
    nums = ['zero','one','two','three','four','five','six','seven','eight','nine','ten', \
    'eleven','twelve','thriteen','fourteen','fifteen','sixteen','seventeen','eighteen','nineteen']
    tens = [None, None,'twenty','thrity','fourty','fifty','sixty','seventy','eighty','ninety']
    try: n = int(n)
    except ValueError: return 'NaN'
    
    if n < 0:
        return 'negitive ' + getNum(abs(n))
    if n < 20: 
        return nums[n]
    if n < 100: # and n >= 20
        s = tens[n//10]
        if n % 10:
            s += ' ' + nums[n%10]
        return s
    if n < 1000: # and n >= 100
        s = nums[n//100] + ' hundred'
        if n % 100:
            s += ' ' + getNum(n - (n//100)*100)
        return s
    if n < 1000000: # and n >= 1000
        s = getNum(n//1000) + ' thousand'
        if n % 1000:
            s += ' ' + getNum(n - (n//1000)*1000)
        return s
    if n < 1000000000: # and n >= 1000000
        s = getNum(n//1000000) + ' million'
        if n % 1000000:
            s += ' ' + getNum(n - (n//1000000)*1000000)
        return s
    if n < 1000000000000: # and n >= 1000000000
        s = getNum(n//1000000000) + ' billion'
        if n % 1000000000:
            s += ' ' + getNum(n - (n//1000000000)*1000000000)
        return s
    if n < 1000000000000000: # and n >= 1000000000
        s = getNum(n//1000000000000) + ' trillion'
        if n % 1000000000000:
            s += ' ' + getNum(n - (n//1000000000000)*1000000000000)
        return s
    else:
        return 'infinity'

def __main__():
    while True:
        i = raw_input("Enter a number or 'q' to quit: ")
        if i in ('q','quit','exit'): break
        print getNum(i)

if __name__ == '__main__': __main__()
