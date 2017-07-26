def format_positive_integer(number):

    l = list(str(number))
    c = len(l)
   
    while c > 3:
        c -= 3
        l.insert(c, '.')

    return ''.join(l)

def format_number(number, precision=0, group_sep='.', decimal_sep=','):

    number = ('%.*f' % (max(0, precision), number)).split('.')

    integer_part = number[0]
    if integer_part[0] == '-':
        sign = integer_part[0]
        integer_part = integer_part[1:]
    else:
        sign = ''
      
    if len(number) == 2:
        decimal_part = decimal_sep + number[1]
    else:
        decimal_part = ''
   
    integer_part = list(integer_part)
    c = len(integer_part)
   
    while c > 3:
        c -= 3
        integer_part.insert(c, group_sep)

    return sign + ''.join(integer_part) + decimal_part
