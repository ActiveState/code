import re

class Scale(str):
    def __len__(self):
        '''
        This ensures that you will always get the actual length of the string,
        minus the extended characters. Which is of course important, when you
        are calculating output field sizes. Requires the re module.
        '''
        tmp = self[:]
        cnt = 0
        for i in re.sub('\\x1b[\[0-9;]*m', '', tmp):
            cnt += 1
        return(cnt)

    def __getattr__(self, method):
        '''
        This is essentially an implimentation of Ruby's .method_missing
        that shortens the code dramatically, and allows for simply extending
        to support other escape codes. As a note, the modifier methods like
        .bold() and .underline() and such, need to come before the color
        methods. The color should always be the last modifier.
        '''
        method_map = {
            'black':     {'color': True,  'value': 30, 'mode': 'm'},
            'red':       {'color': True,  'value': 31, 'mode': 'm'},
            'green':     {'color': True,  'value': 32, 'mode': 'm'},
            'yellow':    {'color': True,  'value': 33, 'mode': 'm'},
            'blue':      {'color': True,  'value': 34, 'mode': 'm'},
            'purple':    {'color': True,  'value': 35, 'mode': 'm'},
            'cyan':      {'color': True,  'value': 36, 'mode': 'm'},
            'white':     {'color': True,  'value': 37, 'mode': 'm'},
            'clean':     {'color': False, 'value': 0,  'mode': 'm'},
            'bold':      {'color': False, 'value': 1,  'mode': 'm'},
            'underline': {'color': False, 'value': 4,  'mode': 'm'},
            'blink':     {'color': False, 'value': 5,  'mode': 'm'},
            'reverse':   {'color': False, 'value': 7,  'mode': 'm'},
            'conceal':   {'color': False, 'value': 8,  'mode': 'm'},
        }

        def get(self, **kwargs):
            if method_map[method]['color']:
                reset='[0m'
            else:
                reset=''

            return(
                Scale('%s[%s%s%s%s' % (
                    reset,
                    method_map[method]['value'],
                    method_map[method]['mode'],
                    self,
                    reset
                )
            ))

        if method in method_map:
            return get.__get__(self)
        else:
            raise(AttributeError, method)
