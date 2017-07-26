# Deveploed by Mark Zitnik

# selected map can be change scrambled
map = ['a','b','c','d','e','f','g','h','i','j','k','l','1','H']

map_dict = {}
base = len(map)

# create a bi-directional dict
for item in range(base):
    map_dict[item] = map[item]
    map_dict[map[item]] = item

def i_to_map_base(num):
    if num == 0: return map_dict[0]
    base_str = []
    while num > 0:
        base_str.append(map_dict[ num % base ])
        num = num / base
    base_str.reverse()
    return ''.join(base_str)

def map_base_to_i(str):
    x = [a for a in str]
    x.reverse()
    value = 0
    for i in range(len(x)):
        item = x[i]
        value += (map_dict[item] * pow(base,i))
    return value

# test code
for i in range(1000):
    str = i_to_map_base(i)
    val = map_base_to_i(str)
    print 'i[%s] : [%s:%s]' % (i , str , val)
