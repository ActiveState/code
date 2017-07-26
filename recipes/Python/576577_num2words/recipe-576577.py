import sys, string as str

words = {
    1 : 'one',
    2 : 'two',
    3 : 'three',
    4 : 'four',
    5 : 'five',
    6 : 'six',
    7 : 'seven',
    8 : 'eight',
    9 : 'nine',
    10 : 'ten',
    11 : 'eleven',
    12 : 'twelve',
    13 : 'thirteen',
    14 : 'fourteen',
    15 : 'fifteen',
    16 : 'sixteen',
    17 : 'seventeen',
    18 : 'eighteen',
    19 : 'nineteen'
}

tens = [
    '',
    'twenty',
    'thirty',
    'forty',
    'fifty',
    'sixty',
    'seventy',
    'eighty',
    'ninety',
]

placeholders = [
    '',
    'thousand',
    'million',
    'billion',
    'trillion',
    'quadrillion'
]

# segMag = segment magnitude (starting at 1)
def convertTrio(number):
    if int(number) < 100:
        return convertDuo(number[1:3])
    else:
        return ' '.join([ words[int(number[0])],  'hundred',  convertDuo(number[1:3]) ])


def convertDuo(number):
    #if teens or less
    if int(number[0]) <= 1:
        return words[int(number)]
    #twenty-five
    else:
        return ''.join([tens[int(number[0]) - 1], '-', words[int(number[1])]])


if __name__ == "__main__":

    string = []
    numeralSegments = []
    numeral = sys.argv[1]

    # left-pad number with zeros to make its length a multiple of 3
    if len(numeral) % 3 > 0:    
        numeral = str.zfill( numeral, (3 - (len(numeral) % 3)) + len(numeral) )

    # split number into lists, grouped in threes
    for i in range (len(numeral), 0, -3):
        numeralSegments.append(numeral[i-3:i])

    # for every segment, convert to trio word and append thousand, million, etc depending on magnitude
    for i in range (len(numeralSegments)):
        string.append(convertTrio(numeralSegments[i]) + ' ' + placeholders[i])

    # reverse the list of strings before concatenating to commas
    string.reverse()        
    print ', '.join(string)
