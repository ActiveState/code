import re
def validate(number):
    'Validates any credit card number using LUHN method'
    number = str(number)
    re.sub(r' ', '', number)
    count = 0
    for i in range(len(number)):
        val = int(number[-(i+1)])
        if i % 2 == 0:
            count += val
        else:
            count += int(str(2 * val)[0])
            if val > 5:
                count += int(str(2 * val)[1])
    if count % 10 == 0:
        return True
    else:
        return False
