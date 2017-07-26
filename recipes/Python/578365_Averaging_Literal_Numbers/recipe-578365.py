import ast

while True:
    try:
        string = raw_input('What numbers should I average? ')
        words = string.split()
        numbers = [ast.literal_eval(word) for word in words]
        total = sum(numbers)
        count = len(numbers)
        average = 1.0 * total / count
        print 'The average is', average
        raw_input('Press enter to quit.')
        break
    except:
        print 'Please only give me numbers.'
