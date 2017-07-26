from dal_1 import DAL1
from math import ceil

################################################################################

class DAL2:

    # CONSTANTS
    MAX_BLOCKS = (2 ** 16) - 1
    MAX_SIZE = (2 ** 16)

    # Disk Abstraction Layer
    def __init__(self, blocks, size):
        assert type(blocks) is int and 1 <= blocks <= self.MAX_BLOCKS
        assert type(size) is int and 1 <= size <= self.MAX_SIZE
        blocks = int(ceil(float(blocks * (size + 1)) / size))
        assert blocks <= self.MAX_SIZE
        DAL1.BLOCKS = blocks
        DAL1.SIZE = size
        self.__disk = DAL1()
        self.__blocks = (blocks * size) / (size + 1)
        self.__index = (blocks - self.__blocks) * size
        self.__BIT = [0 for index in range(self.__blocks)]

    # Open A Block
    def open(self, status):
        assert type(status) is int and 1 <= status <= 255
        index = self.__BIT.index(0)
        self.__BIT[index] = status
        return index

    # Read A Block
    def read(self, block):
        assert type(block) is int and 0 <= block < self.__blocks
        assert self.__BIT[block] != 0
        return self.__disk.read(self.__index + block * self.__disk.SIZE, \
                                self.__disk.SIZE)

    # Write A Block
    def write(self, block, data):
        assert type(block) is int and 0 <= block < self.__blocks
        assert type(data) is str and len(data) == self.__disk.SIZE
        assert self.__BIT[block] != 0
        self.__disk.write(self.__index + block * self.__disk.SIZE, data)

    # Close A Block
    def close(self, block):
        assert type(block) is int and 0 <= block < self.__blocks
        assert self.__BIT[block] != 0
        self.__disk.erase(self.__index + block * self.__disk.SIZE, \
                          self.__disk.SIZE)
        self.__BIT[block] = 0

    # Get Status Information
    def status(self, block):
        assert type(block) is int and 0 <= block < self.__blocks
        return self.__BIT[block]

    # Probability Of Failure
    def fail(self, probability):
        self.__disk.fail(probability)

    # Dump To File
    def dump(self, name):
        self.__disk.write(0, ''.join([chr(i) for i in self.__BIT]))
        self.__disk.dump(name)

    # Load From File
    def load(self, name, abstract):
        assert type(abstract) is bool
        self.__disk.load(name)
        self.__blocks = (self.__disk.BLOCKS * self.__disk.SIZE) / \
                        (self.__disk.SIZE + 1)
        self.__index = (self.__disk.BLOCKS - self.__blocks) * self.__disk.SIZE
        self.__BIT = [ord(c) for c in self.__disk.read(0, self.__blocks)]
        if abstract:
            self.__soft()
        else:
            self.__hard()

    # Fix All Errors
    def __soft(self):
        for block, status in enumerate(self.__BIT):
            if status == 0:
                self.__disk.erase(self.__index + block * self.__disk.SIZE, \
                                  self.__disk.SIZE)

    # Find Any Error
    def __hard(self):
        data = chr(0) * self.__disk.SIZE
        for block, status in enumerate(self.__BIT):
            if status == 0:
                assert data == self.__disk.read(self.__index + block * \
                                                self.__disk.SIZE, \
                                                self.__disk.SIZE)

################################################################################

def test():
    from os import remove, urandom
    from random import randint
    test = DAL2(1024, 1024)
    memo = [None for temp in range(1024)]
    for temp in range(1024):
        status = randint(1, 255)
        block = test.open(status)
        data = urandom(1024)
        test.write(block, data)
        memo[block] = status, data
    for temp in range(1024):
        block = randint(0, 1023)
        if test.status(block):
            test.close(block)
            memo[block] = None
    test.dump('temp')
    other = DAL2(1, 1)
    other.load('temp', False)
    remove('temp')
    try:
        for index, information in enumerate(memo):
            if information is None:
                assert other.status(index) == 0
            else:
                assert other.status(index) == information[0]
                assert other.read(index) == information[1]
        valid = False
        try:
            other.status(1024)
        except:
            valid = True
        assert valid
        raw_input('Tested To True')
    except:
        raw_input('Tested To False')

################################################################################

if __name__ == '__main__':
    test()
