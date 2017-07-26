def frequency_analysis(text):
    '''Counts the frequency of characters within a text

    text -- the text to be analysed

    '''
    import re
    alphabet = {}
    for i in range(26):
        alphabet[chr(65+i)] = 0
    for char in text.upper():
        for i in range(94):
            if chr(33 + i) == char:
                try:
                    alphabet[char] += 1
                except KeyError:
                    alphabet[char] = 1
                break
    re.sub(r'\s', '', text)
    count = len(text)
    for i in range(94):
        char = chr(33+i)
        try:
            print("{} = {}%".format(char, round(alphabet[char] * 100/count, 1)))
        except KeyError:
            pass
        
