#! /usr/bin/python

def print_dict(dictionary, ident = '', braces=1):
    """ Recursively prints nested dictionaries."""

    for key, value in dictionary.iteritems():
        if isinstance(value, dict):
            print '%s%s%s%s' %(ident,braces*'[',key,braces*']') 
            print_dict(value, ident+'  ', braces+1)
        else:
            print ident+'%s = %s' %(key, value)

if __name__ == '__main__':

    example_dict = { 'key1' : 'value1',
                     'key2' : 'value2',
                     'key3' : { 'key3a': 'value3a' },
                     'key4' : { 'key4a': { 'key4aa': 'value4aa',
                                           'key4ab': 'value4ab',
                                           'key4ac': 'value4ac'},
                                'key4b': 'value4b'}
                   }

    print_dict(example_dict)
