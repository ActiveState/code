#This code is GPL3

def calc_check_digit(value):
    """calculate check digit, they are the same for both UPCA and UPCE"""
    check_digit=0
    odd_pos=True
    for char in str(value)[::-1]:
        if odd_pos:
            check_digit+=int(char)*3
        else:
            check_digit+=int(char)
        odd_pos=not odd_pos #alternate
    check_digit=check_digit % 10
    check_digit=10-check_digit
    check_digit=check_digit % 10
    return check_digit

def convert_UPCE_to_UPCA(upce_value):
    """Test value 04182635 -> 041800000265"""
    if len(upce_value)==6:
        middle_digits=upce_value #assume we're getting just middle 6 digits
    elif len(upce_value)==7:
        #truncate last digit, assume it is just check digit
        middle_digits=upce_value[:6]
    elif len(upce_value)==8:
        #truncate first and last digit, 
        #assume first digit is number system digit
        #last digit is check digit
        middle_digits=upce_value[1:7]
    else:
        return False
    d1,d2,d3,d4,d5,d6=list(middle_digits)
    if d6 in ["0","1","2"]:
        mfrnum=d1+d2+d6+"00"
        itemnum="00"+d3+d4+d5
    elif d6=="3":
        mfrnum=d1+d2+d3+"00"
        itemnum="000"+d4+d5        
    elif d6=="4":
        mfrnum=d1+d2+d3+d4+"0"
        itemnum="0000"+d5    
    else:
        mfrnum=d1+d2+d3+d4+d5
        itemnum="0000"+d6
    newmsg="0"+mfrnum+itemnum
    #calculate check digit, they are the same for both UPCA and UPCE
    check_digit=calc_check_digit(newmsg)
    return newmsg+str(check_digit)

#Usage example
print convert_UPCE_to_UPCA(UPCE)
