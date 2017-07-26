def keynat(string):
        '''A natural sort helper function for sort() and sorted()
        without using regular expression.
        '''
        r = []
        for c in string:
                if c.isdigit():
                        if r and isinstance(r[-1], int):
                                r[-1] = r[-1] * 10 + int(c)
                        else:
                                r.append(int(c))
                else:
                        r.append(c)
        return r
