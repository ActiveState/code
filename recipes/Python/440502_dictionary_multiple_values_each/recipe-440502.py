class mdict(dict):

    def __setitem__(self, key, value):
        """add the given value to the list of values for this key"""
        self.setdefault(key, []).append(value)

 
if __name__ == '__main__':
    ml = mdict()
    key = 'key'
    ml[key] = 'val1' 
    ml[key] = 'val2'
    print ml[key]

    
