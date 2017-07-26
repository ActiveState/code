def part1by1(n):
        n&= 0x0000ffff
        n = (n | (n << 8)) & 0x00FF00FF
        n = (n | (n << 4)) & 0x0F0F0F0F
        n = (n | (n << 2)) & 0x33333333
        n = (n | (n << 1)) & 0x55555555
        return n


def unpart1by1(n):
        n&= 0x55555555
        n = (n ^ (n >> 1)) & 0x33333333
        n = (n ^ (n >> 2)) & 0x0f0f0f0f
        n = (n ^ (n >> 4)) & 0x00ff00ff
        n = (n ^ (n >> 8)) & 0x0000ffff
        return n


def interleave2(x, y):
        return part1by1(x) | (part1by1(y) << 1)


def deinterleave2(n):
        return unpart1by1(n), unpart1by1(n >> 1)


def part1by2(n):
        n&= 0x000003ff
        n = (n ^ (n << 16)) & 0xff0000ff
        n = (n ^ (n <<  8)) & 0x0300f00f
        n = (n ^ (n <<  4)) & 0x030c30c3
        n = (n ^ (n <<  2)) & 0x09249249
        return n


def unpart1by2(n):
        n&= 0x09249249
        n = (n ^ (n >>  2)) & 0x030c30c3
        n = (n ^ (n >>  4)) & 0x0300f00f
        n = (n ^ (n >>  8)) & 0xff0000ff
        n = (n ^ (n >> 16)) & 0x000003ff
        return n


def interleave3(x, y, z):
        return part1by2(x) | (part1by2(y) << 1) | (part1by2(z) << 2)


def deinterleave3(n):
        return unpart1by2(n), unpart1by2(n >> 1), unpart1by2(n >> 2)
