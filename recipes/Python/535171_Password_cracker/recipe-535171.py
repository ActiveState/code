import os

from commands import getoutput

leet = {
    'a': ('a', 'A', '4'),
    'b': ('B', '3', '8'),
    'c': ('c', 'C', 'k', 'K'),
    'd': ('d', 'D', ),
    'e': ('e', 'E', '3'),
    'f': ('f', 'F', ),
    'g': ('g', 'G', '6'),
    'h': ('h', 'H', '4'),
    'i': ('i', 'I', '1', '!', 'l'),
    'j': ('j', 'J', ),
    'k': ('k', 'K', 'c', 'C'),
    'l': ('l', 'L', ),
    'm': ('m', 'M', ),
    'n': ('n', 'N', ),
    'o': ('o', 'O', '0', ),
    'p': ('p', 'P', '9', ),
    'q': ('q', 'Q', '9', 'k', 'K', ),
    'r': ('r', 'R', ),
    's': ('s', 'S', '5', 'z', 'Z'),
    't': ('t', 'T', '7', '4'),
    'u': ('u', 'U', 'v', 'V'),
    'v': ('v', 'V', 'u', 'U'),
    'w': ('w', 'W', ),
    'x': ('x', 'X', ),
    'y': ('y', 'Y', ),
    'z': ('z', 'Z', 's', 'S', '5'),
}
    
command = 'openssl rsa -in mysecuresite.com.key -out tmp.key -passin pass:%s'
passwdBasic = 'thisisnottherealpassword'

def main():
    arrays = [leet[ltr] for ltr in passwdBasic]
    start = [ltrs[0] for ltrs in arrays]
    end = [ltrs[-1] for ltrs in arrays]
    indexes = [0] * len(arrays)
    maxes = [len(ltrs)-1 for ltrs in arrays]
    chrs = [ltrs[i] for ltrs, i in zip(arrays, indexes)]
    while chrs != end:
        passx = ''.join(chrs)
        open('tries.txt', 'a+').write(passx + '\n')
        out = getoutput(command)
        if 'bad decrypt' not in out:
            print 'GOT IT!', passx
            return
        # Next letter
        for i in range(len(indexes)-1, -1, -1):
            if indexes[i] <= maxes[i]-1:
                indexes[i] += 1
                break
            else:
                indexes[i] = 0
        # Make up the chrs
        chrs = [ltrs[i] for ltrs, i in zip(arrays, indexes)]


if __name__ == '__main__':
    main()
