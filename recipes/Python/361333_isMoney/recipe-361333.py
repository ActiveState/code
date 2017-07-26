# isMoney.py
'''A simple program to check a data is in money datatype'''

def isMoney():
#   format = "123.45"
    money = 123
    flag = 0
    
    # check - all is digits ?
    if str(money).isdigit() == 1:
        flag = 1 
    else:
        # loop into the data
        for i in range (0, len(str(money)) + 1):
            # check - decimal point exists ?
            if str(money)[i:i+1] == ".":
                # check - all is digits (except the ".") ?
                if str(money)[i+1:].isdigit() == 1 and str(money)[:i].isdigit() == 1:
                    flag = 1

    # check - is money ?
    if flag == 1:
        print "$" + "%.2f" % float(money)
    else:
        print money, "is not money datatype"

    
if __name__ == '__main__':
    isMoney()
