def dsvgen(filename,separator='|'):
    """generates a list of values for each line in a dsv file

    >>> for row in dsvgen('myfilename'): print row
    """
    inpfile=open(filename)
    for line in inpfile:
        yield line.strip().split(separator)
    inpfile.close()
