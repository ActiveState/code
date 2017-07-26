import math

def int_to_bytes_needed(integer):
    bytes_needed = math.pow((integer + 1),.125)/2
    rounded_bytes_to_whole = math.ceil(bytes_needed)
    return rounded_bytes_to_whole


# One-liner versoins:

# required_bytes = lambda x: ((((x+1)**.125)/2)//1)+1
# required_bytes(INTEGER_GOES_HERE)

# or:

# ((((INTEGER_GOES_HERE +1 )**.125)/2)//1) + 1
