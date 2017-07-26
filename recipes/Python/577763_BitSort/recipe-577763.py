#-*-coding:utf-8-*-

from bitarray import bitarray

def bitsort(list_to_sort):
    a = bitarray(max(list_to_sort)+1)
    a.setall(False)
    for n in list_to_sort:
        a[n] = True
    return [i for i,val in enumerate(a) if val]


if __name__ == "__main__":
    print bitsort([17, 8, 27, 16, 26, 1, 5, 0, 24])
