from random import random

################################################################################

class DiskDriver:

    # CONSTANTS
    MAX_BLOCKS = (2 ** 16)
    MAX_SIZE = (2 ** 16)
    MAX_WORD = (2 ** 16) - 1

    # Disk With Driver
    def __init__(self, blocks, size):
        assert type(blocks) is int and 1 <= blocks <= self.MAX_BLOCKS
        assert type(size) is int and 1 <= size <= self.MAX_SIZE
        self.__blocks = blocks
        self.__size = size
        self.__fail = float()
        self.__disk = dict()

    # Read A Block
    def read(self, block):
        assert type(block) is int and 1 <= block <= self.__blocks
        assert self.__fail <= random()
        if self.__disk.has_key(block):
            return self.__disk[block]
        else:
            return chr(0) * self.__size

    # Write A Block
    def write(self, block, data):
        assert type(block) is int and 1 <= block <= self.__blocks
        assert type(data) is str and len(data) == self.__size
        assert self.__fail <= random()
        self.__disk[block] = data

    # Erase A Block
    def erase(self, block):
        assert type(block) is int and 1 <= block <= self.__blocks
        assert self.__fail <= random()
        if self.__disk.has_key(block):
            del self.__disk[block]

    # Probability Of Failure
    def fail(self, probability):
        assert type(probability) is float and 0 <= probability <= 1
        self.__fail = float(int(probability * self.MAX_WORD)) / self.MAX_WORD

    # Dump To File
    def dump(self, name):
        assert type(name) is str
        pickle = file(name, 'wb')
        temp = self.__blocks - 1
        pickle.write(chr(temp >> 8) + chr(temp & 0xFF))
        temp = self.__size - 1
        pickle.write(chr(temp >> 8) + chr(temp & 0xFF))
        temp = int(self.__fail * self.MAX_WORD)
        pickle.write(chr(temp >> 8) + chr(temp & 0xFF))
        for key in self.__disk:
            temp = key - 1
            pickle.write(chr(temp >> 8) + chr(temp & 0xFF))
            pickle.write(self.__disk[key])
        pickle.close()

    # Load From File
    def load(self, name):
        assert type(name) is str
        pickle = file(name, 'rb')
        temp = pickle.read(2)
        assert len(temp) == 2
        self.__blocks = (ord(temp[0]) << 8) + (ord(temp[1]) + 1)
        temp = pickle.read(2)
        assert len(temp) == 2
        self.__size = (ord(temp[0]) << 8) + (ord(temp[1]) + 1)
        temp = pickle.read(2)
        assert len(temp) == 2
        self.__fail = float((ord(temp[0]) << 8) + ord(temp[1])) / self.MAX_WORD
        self.__disk = dict()
        while True:
            temp = pickle.read(2)
            if not temp:
                break
            assert len(temp) == 2
            key = (ord(temp[0]) << 8) + (ord(temp[1]) + 1)
            assert 1 <= key <= self.__blocks
            temp = pickle.read(self.__size)
            assert len(temp) == self.__size
            self.__disk[key] = temp
        pickle.close()

    # Test If Equal
    def __eq__(self, other):
        try:
            assert self.__blocks == other.__blocks
            assert self.__size == other.__size
            assert self.__fail == other.__fail
            assert len(self.__disk) == len(other.__disk)
            for key in self.__disk:
                assert self.__disk[key] == other.__disk[key]
            return True
        except:
            return False

################################################################################

def test():
    from os import remove, urandom
    from random import randint
    test = DiskDriver(1024, 1024)
    for temp in range(512):
        test.write(randint(1, 1024), urandom(1024))
    test.dump('temp')
    other = DiskDriver(1, 1)
    other.load('temp')
    remove('temp')
    raw_input('Tested To ' + str(test == other))

################################################################################

if __name__ == '__main__':
    test()
