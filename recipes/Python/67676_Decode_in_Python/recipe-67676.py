def decode(*arguments):
    """Compares first item to subsequent item one by one.

    If first item is equal to a key, returns the corresponding value (next item).
    If no match is found, returns None, or, if default is omitted, returns None.
    """
    if len(arguments) < 3:
        raise TypeError, 'decode() takes at least 3 arguments (%d given)' % (len(arguments))
    dict = list(arguments[1:])
    if arguments[0] in dict:
        index = dict.index(arguments[0]);
        if index % 2 == 0 and len(dict) > index+1:
            return dict[index+1]
        return dict[-1]
    elif len(dict) % 2 != 0:
        return dict[-1]

# example usage
return_value = decode('b', 'a', 1, 'b', 2, 3)

var = 'list'
return_type = decode(var, 'tuple', (), 'dict', {}, 'list', [], 'string', '')
