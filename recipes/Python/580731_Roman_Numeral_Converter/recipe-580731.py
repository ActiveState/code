#Roman Numeral Converter
#Written By Brandon Martin
#Digital Sol

class IllegalCharacterError(Exception):
    pass

def romanToNumber(numerals):
    '''Converts a string of Roman Numerals (I,V,X,L,C,D,M) into an integer.'''

    romanConversionTable = {
        'I' : 1,
        'V' : 5,
        'X' : 10,
        'L' : 50,
        'C' : 100,
        'D' : 500,
        'M' : 1000
    }

    ### Build List of Numbers ###
    
    numberList = []
    for letter in numerals:
        # Build List of Numbers
        if letter in romanConversionTable:
            numberList += [romanConversionTable[letter]]
        else:
            raise IllegalCharacterError('{} is not a Roman Numeral'.format(letter))

    if len(numberList) == 1:
        return numberList[0]

    ### Construct Final Total ###

    previous = numberList[-1]
    total = previous
    for current in range(len(numberList)-2,-1, -1):
        if numberList[current] < previous:
            total -= numberList[current]
        else:
            total += numberList[current]
        previous = numberList[current]

    return total

def numberToRoman(integer):
    '''Converts an integer into a string of Roman Numerals.'''

    if type(integer) != int:
        raise TypeError('Input must be an integer.')
    
    numberConversionTable = {
        1 : 'I',
        5 : 'V',
        10 : 'X',
        50 : 'L',
        100 : 'C',
        500 : 'D',
        1000 : 'M'
    }
    quads = ('I','X','C')
    doubs = ('V','L','D')
    foundNumeral = ''
    found = 0

    ### Build List of Roman Numerals ###

    numeralList = []
    for value in [1000,500,100,50,10,5,1]:
        while integer >= value:
            integer -= value
            numeralList += [numberConversionTable[value]]
    if len(numeralList) == 1: #Return result if only one symbol
        return numeralList.pop()

    ### Modify List to Proper Formatting ###

    finalNumeralList = []
    repeats = 0

    for numeral in numeralList:
        if len(finalNumeralList) == 0:
            # ADD FIRST NUMBER
            finalNumeralList += [numeral]
        else:
            if numeral != finalNumeralList[len(finalNumeralList)-1]:
                # CURRENT NUMERAL IS DIFFERENT FROM THE LAST
                if 3 > repeats > 0:
                    # ADD IN ALL REPEATS
                    for i in range(repeats):
                        finalNumeralList += [finalNumeralList[-1]]
                repeats = 0
                finalNumeralList += [numeral]
            else:
                # CURRENT NUMERAL IS THE SAME AS THE LAST
                repeats += 1
                if repeats == 3 and numeral != 'M':
                    # EXCHANGE THREE ONES NUMERALS FOR ONE FIVES NUMERAL
                    modifiedNumeral = doubs[quads.index(numeral)]
                    if modifiedNumeral == finalNumeralList[len(finalNumeralList)-2]:
                        # NUMERALS IN A THREE DIGIT RANGE ADD TO 9
                        finalNumeralList.pop(len(finalNumeralList)-2)
                        if numeral != 'C':
                            finalNumeralList += [quads[quads.index(numeral)+1]]
                        else:
                            finalNumeralList += ['M']
                    else:
                        finalNumeralList += [modifiedNumeral]
                    repeats = 0
                elif numeral == 'M':
                    # AUTOMATICALLY ADD M
                    finalNumeralList += ['M']
                    repeats = 0
                    
    if repeats > 0:
        # ADD IN ANY REMAINING REPEATS
        for i in range(repeats):
            finalNumeralList += [finalNumeralList[-1]]
                        
    finalString = ''.join(finalNumeralList)
                                                        
    return finalString
