def ReverseByteOrder(data):
    """
    Method to reverse the byte order of a given unsigned data value
    Input:
        data:   data value whose byte order needs to be swap
                data can only be as big as 4 bytes
    Output:
        revD: data value with its byte order reversed
    """
    s = "Error: Only 'unsigned' data of type 'int' or 'long' is allowed"
    if not ((type(data) == int)or(type(data) == long)):
        s1 = "Error: Invalid data type: %s" % type(data)
        print(''.join([s,'\n',s1]))
        return data
    if(data < 0):
        s2 = "Error: Data is signed. Value is less than 0"
        print(''.join([s,'\n',s2]))
        return data

    seq = ["0x"]

    while(data > 0):
        d = data & 0xFF     # extract the least significant(LS) byte
        seq.append('%02x'%d)# convert to appropriate string, append to sequence
        data >>= 8          # push next higher byte to LS position

    revD = int(''.join(seq),16)

    return revD
