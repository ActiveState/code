# Guyon Morée
# http://gumuz.looze.net/

def Binary2Decimal(bin_num):
    """ Return the decimal representation of bin_num
    
        This actually uses the built-in int() function, 
        but is wrapped in a function for consistency """
    return int(bin_num, 2)


def Decimal2Binary(dec_num):
    """ Return the binary representation of dec_num """
    if dec_num == 0: return '0'
    return (Decimal2Binary(dec_num >> 1) + str(dec_num % 2))
