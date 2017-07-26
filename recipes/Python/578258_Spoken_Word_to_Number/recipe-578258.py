import re
_known = {
    'zero': 0,
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
    'ten': 10,
    'eleven': 11,
    'twelve': 12,
    'thirteen': 13,
    'fourteen': 14,
    'fifteen': 15,
    'sixteen': 16,
    'seventeen': 17,
    'eighteen': 18,
    'nineteen': 19,
    'twenty': 20,
    'thirty': 30,
    'forty': 40,
    'fifty': 50,
    'sixty': 60,
    'seventy': 70,
    'eighty': 80,
    'ninety': 90
    }
def spoken_word_to_number(n):
    """Assume n is a positive integer".
assert _positive_integer_number('nine hundred') == 900
assert spoken_word_to_number('one hundred') == 100
assert spoken_word_to_number('eleven') == 11
assert spoken_word_to_number('twenty two') == 22
assert spoken_word_to_number('thirty-two') == 32
assert spoken_word_to_number('forty two') == 42
assert spoken_word_to_number('two hundred thirty two') == 232
assert spoken_word_to_number('two thirty two') == 232
assert spoken_word_to_number('nineteen hundred eighty nine') == 1989
assert spoken_word_to_number('nineteen eighty nine') == 1989
assert spoken_word_to_number('one thousand nine hundred and eighty nine') == 1989
assert spoken_word_to_number('nine eighty') == 980
assert spoken_word_to_number('nine two') == 92 # wont be able to convert this one
assert spoken_word_to_number('nine thousand nine hundred') == 9900
assert spoken_word_to_number('one thousand nine hundred one') == 1901
"""

    n = n.lower().strip()
    if n in _known:
        return _known[n]
    else:
        inputWordArr = re.split('[ -]', n)

    assert len(inputWordArr) > 1 #all single words are known
    #Check the pathological case where hundred is at the end or thousand is at end
    if inputWordArr[-1] == 'hundred':
        inputWordArr.append('zero')
        inputWordArr.append('zero')
    if inputWordArr[-1] == 'thousand':
        inputWordArr.append('zero')
        inputWordArr.append('zero')
        inputWordArr.append('zero')
    if inputWordArr[0] == 'hundred':
        inputWordArr.insert(0, 'one')
    if inputWordArr[0] == 'thousand':
        inputWordArr.insert(0, 'one')

    inputWordArr = [word for word in inputWordArr if word not in ['and', 'minus', 'negative']]
    currentPosition = 'unit'
    prevPosition = None
    output = 0
    for word in reversed(inputWordArr):
        if currentPosition == 'unit':
            number = _known[word]
            output += number
            if number > 9:
                currentPosition = 'hundred'
            else:
                currentPosition = 'ten'
        elif currentPosition == 'ten':
            if word != 'hundred':
                number = _known[word]
                if number < 10:
                    output += number*10
                else:
                    output += number
            #else: nothing special
            currentPosition = 'hundred'
        elif currentPosition == 'hundred':
            if word not in [ 'hundred', 'thousand']:
                number = _known[word]
                output += number*100
                currentPosition = 'thousand'
            elif word == 'thousand':
                currentPosition = 'thousand'
            else:
                currentPosition = 'hundred'
        elif currentPosition == 'thousand':
            assert word != 'hundred'
            if word != 'thousand':
                number = _known[word]
                output += number*1000
        else:
            assert "Can't be here" == None

    return(output)
