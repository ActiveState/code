import dal_2
from math import ceil

################################################################################

class DAL2(dal_2.DAL2):

    # Get Configuration Information
    def info(self):
        return self.__blocks, self.__disk.SIZE

    # Change Status Information
    def edit(self, block, status):
        assert type(block) is int and 0 <= block < self.__blocks
        assert type(status) is int and 1 <= status <= 255
        assert self.__BIT[block] != 0
        self.__BIT[block] = status

################################################################################

class Seed:

    # Random Seed Generator
    def __init__(self, data):
        if type(data) is int:
            assert 1 <= data <= 65536
            self.__data = [0 for index in range(data)]
        elif type(data) is str:
            assert 1 <= len(data) <= 65536
            self.__data = [ord(c) for c in data]
        else:
            raise TypeError
        self.__active = True
        self.__index = 0

    # Seed Control Interface
    def __call__(self, data=None):
        if data is None:
            return ''.join([chr(i) for i in self.__data])
        elif type(data) is bool:
            self.__active = data
        elif type(data) is str:
            if self.__active:
                for c in data:
                    self.__data[self.__index] ^= ord(c)
                    self.__index = (self.__index + 1) % len(self.__data)
        else:
            raise TypeError

################################################################################

# Create Enumeration Objects
def enum(*names):
    class enum:
        def __setattr__(self, name, value):
            raise AttributeError
        def __delattr__(self, name):
            raise AttributeError
    temp = enum()
    for value, name in enumerate(names):
        temp.__dict__[name] = value
    return temp

################################################################################

class DAL3:

    # CONSTANTS
    MAX_BLOCKS = (2 ** 16) - 2
    MAX_SIZE = (2 ** 16)
    STATUS = enum('closed', 'd1', 'dA', 'dB', 'dZ', \
                  'f1', 'fA', 'fB', 'fZ', 'b1', 's1')

    # Disk Abstraction Layer
    def __init__(self, blocks, size):
        assert type(blocks) is int and 0 < blocks <= self.MAX_BLOCKS
        assert type(size) is int and 4 < size <= self.MAX_SIZE
        blocks += 1
        assert int(ceil(float(blocks * (size + 1)) / size)) <= self.MAX_SIZE
        self.__disk = DAL2(blocks, size)
        self.__blocks, self.__size = self.__disk.info()
        self.__blocks -= 1
        self.__seed = Seed(self.__size)
        self.__disk.open(self.STATUS.s1)

    # Open A Directory
    def open_directory(self):
        return self.__disk.open(self.STATUS.d1)

    # Read A Directory
    def read_directory(self, block):
        assert type(block) is int and 1 <= block <= self.__blocks
        status = self.__disk.status(block)
        assert self.STATUS.d1 <= status <= self.STATUS.dZ
        if status == self.STATUS.d1:
            temp = self.__disk.read(block)
            size = (ord(temp[0]) << 8) + ord(temp[1])
            return temp[2:size+2]
        else:
            while self.__disk.status(block) != self.STATUS.dA:
                temp = self.__disk.read(block)
                block = (ord(temp[0]) << 8) + ord(temp[1])
            temp = self.__disk.read(block)
            size = (ord(temp[0]) << 8) + ord(temp[1])
            data = temp[2:-2]
            block = (ord(temp[-2]) << 8) + ord(temp[-1])
            while self.__disk.status(block) == self.STATUS.dB:
                temp = self.__disk.read(block)
                data += temp[2:-2]
                block = (ord(temp[-2]) << 8) + ord(temp[-1])
            temp = self.__disk.read(block)
            return data + temp[2:size-len(data)+2]

    # Write A Directory
    def write_directory(self, block, data):
        assert type(block) is int and 1 <= block <= self.__blocks
        assert type(data) is str and len(data)
        status = self.__disk.status(block)
        assert self.STATUS.d1 <= status <= self.STATUS.dZ
        self.__seed(data)
        dir_map = [block]
        if status == self.STATUS.dA:
            temp = self.__disk.read(block)
            block = (ord(temp[-2]) << 8) + ord(temp[-1])
            dir_map = dir_map + [block]
            while self.__disk.status(block) == self.STATUS.dB:
                temp = self.__disk.read(block)
                block = (ord(temp[-2]) << 8) + ord(temp[-1])
                dir_map = dir_map + [block]
        elif status == self.STATUS.dB:
            temp = self.__disk.read(block)
            dirA = (ord(temp[0]) << 8) + ord(temp[1])
            dir_map = [dirA] + dir_map
            dirZ = (ord(temp[-2]) << 8) + ord(temp[-1])
            dir_map = dir_map + [dirZ]
            while self.__disk.status(dirA) == self.STATUS.dB:
                temp = self.__disk.read(dirA)
                dirA = (ord(temp[0]) << 8) + ord(temp[1])
                dir_map = [dirA] + dir_map
            while self.__disk.status(dirZ) == self.STATUS.dB:
                temp = self.__disk.read(dirZ)
                dirZ = (ord(temp[-2]) << 8) + ord(temp[-1])
                dir_map = dir_map + [dirZ]
        elif status == self.STATUS.dZ:
            temp = self.__disk.read(block)
            block = (ord(temp[0]) << 8) + ord(temp[1])
            dir_map = [block] + dir_map
            while self.__disk.status(block) == self.STATUS.dB:
                temp = self.__disk.read(block)
                block = (ord(temp[0]) << 8) + ord(temp[1])
                dir_map = [block] + dir_map
        size = self.__size - 4
        if len(data) % size:
            blocks = len(data) / size + 1
        else:
            blocks = len(data) / size
        blocks = [data[index*size:index*size+size] for index in range(blocks)]
        while len(dir_map) > len(blocks):
            self.__disk.close(dir_map[-1])
            del dir_map[-1]
        while len(dir_map) < len(blocks):
            dir_map.append(self.__disk.open(255))
        if len(blocks) == 1:
            temp = len(data)
            size = chr(temp >> 8) + chr(temp & 0xFF)
            blocks[0] = size + blocks[0] + size
        else:
            temp = len(data)
            size = chr(temp >> 8) + chr(temp & 0xFF)
            temp = dir_map[1]
            next = chr(temp >> 8) + chr(temp & 0xFF)
            blocks[0] = size + blocks[0] + next
            index = 1
            while blocks[index] is not blocks[-1]:
                temp = dir_map[index - 1]
                last = chr(temp >> 8) + chr(temp & 0xFF)
                temp = dir_map[index + 1]
                next = chr(temp >> 8) + chr(temp & 0xFF)
                blocks[index] = last + blocks[index] + next
                index += 1
            temp = dir_map[index - 1]
            last = chr(temp >> 8) + chr(temp & 0xFF)
            blocks[index] = last + blocks[index] + size
        if len(blocks) == 1:
            self.__disk.write(dir_map[0], blocks[0] + chr(0) * \
                              (self.__size - len(blocks[0])))
            self.__disk.edit(dir_map[0], self.STATUS.d1)
        else:
            self.__disk.write(dir_map[0], blocks[0])
            self.__disk.edit(dir_map[0], self.STATUS.dA)
            index = 1
            while blocks[index] is not blocks[-1]:
                self.__disk.write(dir_map[index], blocks[index])
                self.__disk.edit(dir_map[index], self.STATUS.dB)
                index += 1
            self.__disk.write(dir_map[index], blocks[index] + chr(0) * \
                              (self.__size - len(blocks[index])))
            self.__disk.edit(dir_map[index], self.STATUS.dZ)

    # Close A Directory
    def close_directory(self, block):
        assert type(block) is int and 1 <= block <= self.__blocks
        status = self.__disk.status(block)
        assert self.STATUS.d1 <= status <= self.STATUS.dZ
        if status == self.STATUS.dA:
            temp = self.__disk.read(block)
            self.__disk.close(block)
            block = (ord(temp[-2]) << 8) + ord(temp[-1])
            while self.__disk.status(block) == self.STATUS.dB:
                temp = self.__disk.read(block)
                self.__disk.close(block)
                block = (ord(temp[-2]) << 8) + ord(temp[-1])
            self.__disk.close(block)
        elif status == self.STATUS.dB:
            temp = self.__disk.read(block)
            self.__disk.close(block)
            dirA = (ord(temp[0]) << 8) + ord(temp[1])
            dirZ = (ord(temp[-2]) << 8) + ord(temp[-1])
            while self.__disk.status(dirA) == self.STATUS.dB:
                temp = self.__disk.read(dirA)
                self.__disk.close(dirA)
                dirA = (ord(temp[0]) << 8) + ord(temp[1])
            self.__disk.close(dirA)
            while self.__disk.status(dirZ) == self.STATUS.dB:
                temp = self.__disk.read(dirZ)
                self.__disk.close(dirZ)
                dirZ = (ord(temp[-2]) << 8) + ord(temp[-1])
            self.__disk.close(dirZ)
        elif status == self.STATUS.dZ:
            temp = self.__disk.read(block)
            self.__disk.blose(block)
            block = (ord(temp[0]) << 8) + ord(temp[1])
            while self.__disk.status(block) == self.STATUS.dB:
                temp = self.__disk.read(block)
                self.__disk.close(block)
                block = (ord(temp[0]) << 8) + ord(temp[1])
            self.__disk.close(block)
        else:
            self.__disk.close(block)

    # Open A File
    def open_file(self):
        return self.__disk.open(self.STATUS.f1)

    # Read A File
    def read_file(self, block):
        assert type(block) is int and 1 <= block <= self.__blocks
        status = self.__disk.status(block)
        assert self.STATUS.f1 <= status <= self.STATUS.fZ
        if status == self.STATUS.f1:
            temp = self.__disk.read(block)
            size = (ord(temp[0]) << 8) + ord(temp[1])
            return temp[2:size+2]
        else:
            while self.__disk.status(block) != self.STATUS.fA:
                temp = self.__disk.read(block)
                block = (ord(temp[0]) << 8) + ord(temp[1])
            temp = self.__disk.read(block)
            size = (ord(temp[0]) << 8) + ord(temp[1])
            data = temp[2:-2]
            block = (ord(temp[-2]) << 8) + ord(temp[-1])
            while self.__disk.status(block) == self.STATUS.fB:
                temp = self.__disk.read(block)
                data += temp[2:-2]
                block = (ord(temp[-2]) << 8) + ord(temp[-1])
            temp = self.__disk.read(block)
            return data + temp[2:size-len(data)+2]

    # Write A File
    def write_file(self, block, data):
        assert type(block) is int and 1 <= block <= self.__blocks
        assert type(data) is str and len(data)
        status = self.__disk.status(block)
        assert self.STATUS.f1 <= status <= self.STATUS.fZ
        self.__seed(data)
        dir_map = [block]
        if status == self.STATUS.fA:
            temp = self.__disk.read(block)
            block = (ord(temp[-2]) << 8) + ord(temp[-1])
            dir_map = dir_map + [block]
            while self.__disk.status(block) == self.STATUS.fB:
                temp = self.__disk.read(block)
                block = (ord(temp[-2]) << 8) + ord(temp[-1])
                dir_map = dir_map + [block]
        elif status == self.STATUS.fB:
            temp = self.__disk.read(block)
            dirA = (ord(temp[0]) << 8) + ord(temp[1])
            dir_map = [dirA] + dir_map
            dirZ = (ord(temp[-2]) << 8) + ord(temp[-1])
            dir_map = dir_map + [dirZ]
            while self.__disk.status(dirA) == self.STATUS.fB:
                temp = self.__disk.read(dirA)
                dirA = (ord(temp[0]) << 8) + ord(temp[1])
                dir_map = [dirA] + dir_map
            while self.__disk.status(dirZ) == self.STATUS.fB:
                temp = self.__disk.read(dirZ)
                dirZ = (ord(temp[-2]) << 8) + ord(temp[-1])
                dir_map = dir_map + [dirZ]
        elif status == self.STATUS.fZ:
            temp = self.__disk.read(block)
            block = (ord(temp[0]) << 8) + ord(temp[1])
            dir_map = [block] + dir_map
            while self.__disk.status(block) == self.STATUS.fB:
                temp = self.__disk.read(block)
                block = (ord(temp[0]) << 8) + ord(temp[1])
                dir_map = [block] + dir_map
        size = self.__size - 4
        if len(data) % size:
            blocks = len(data) / size + 1
        else:
            blocks = len(data) / size
        blocks = [data[index*size:index*size+size] for index in range(blocks)]
        while len(dir_map) > len(blocks):
            self.__disk.close(dir_map[-1])
            del dir_map[-1]
        while len(dir_map) < len(blocks):
            dir_map.append(self.__disk.open(255))
        if len(blocks) == 1:
            temp = len(data)
            size = chr(temp >> 8) + chr(temp & 0xFF)
            blocks[0] = size + blocks[0] + size
        else:
            temp = len(data)
            size = chr(temp >> 8) + chr(temp & 0xFF)
            temp = dir_map[1]
            next = chr(temp >> 8) + chr(temp & 0xFF)
            blocks[0] = size + blocks[0] + next
            index = 1
            while blocks[index] is not blocks[-1]:
                temp = dir_map[index - 1]
                last = chr(temp >> 8) + chr(temp & 0xFF)
                temp = dir_map[index + 1]
                next = chr(temp >> 8) + chr(temp & 0xFF)
                blocks[index] = last + blocks[index] + next
                index += 1
            temp = dir_map[index - 1]
            last = chr(temp >> 8) + chr(temp & 0xFF)
            blocks[index] = last + blocks[index] + size
        if len(blocks) == 1:
            self.__disk.write(dir_map[0], blocks[0] + chr(0) * \
                              (self.__size - len(blocks[0])))
            self.__disk.edit(dir_map[0], self.STATUS.f1)
        else:
            self.__disk.write(dir_map[0], blocks[0])
            self.__disk.edit(dir_map[0], self.STATUS.fA)
            index = 1
            while blocks[index] is not blocks[-1]:
                self.__disk.write(dir_map[index], blocks[index])
                self.__disk.edit(dir_map[index], self.STATUS.fB)
                index += 1
            self.__disk.write(dir_map[index], blocks[index] + chr(0) * \
                              (self.__size - len(blocks[index])))
            self.__disk.edit(dir_map[index], self.STATUS.fZ)

    # Close A File
    def close_file(self, block):
        assert type(block) is int and 1 <= block <= self.__blocks
        status = self.__disk.status(block)
        assert self.STATUS.f1 <= status <= self.STATUS.fZ
        if status == self.STATUS.fA:
            temp = self.__disk.read(block)
            self.__disk.close(block)
            block = (ord(temp[-2]) << 8) + ord(temp[-1])
            while self.__disk.status(block) == self.STATUS.fB:
                temp = self.__disk.read(block)
                self.__disk.close(block)
                block = (ord(temp[-2]) << 8) + ord(temp[-1])
            self.__disk.close(block)
        elif status == self.STATUS.fB:
            temp = self.__disk.read(block)
            self.__disk.close(block)
            dirA = (ord(temp[0]) << 8) + ord(temp[1])
            dirZ = (ord(temp[-2]) << 8) + ord(temp[-1])
            while self.__disk.status(dirA) == self.STATUS.fB:
                temp = self.__disk.read(dirA)
                self.__disk.close(dirA)
                dirA = (ord(temp[0]) << 8) + ord(temp[1])
            self.__disk.close(dirA)
            while self.__disk.status(dirZ) == self.STATUS.fB:
                temp = self.__disk.read(dirZ)
                self.__disk.close(dirZ)
                dirZ = (ord(temp[-2]) << 8) + ord(temp[-1])
            self.__disk.close(dirZ)
        elif status == self.STATUS.fZ:
            temp = self.__disk.read(block)
            self.__disk.blose(block)
            block = (ord(temp[0]) << 8) + ord(temp[1])
            while self.__disk.status(block) == self.STATUS.fB:
                temp = self.__disk.read(block)
                self.__disk.close(block)
                block = (ord(temp[0]) << 8) + ord(temp[1])
            self.__disk.close(block)
        else:
            self.__disk.close(block)

    # Open A Block
    def open_block(self):
        return self.__disk.open(self.STATUS.b1)

    # Read A Block
    def read_block(self, block):
        assert type(block) is int and 1 <= block <= self.__blocks
        assert self.__disk.status(block) == self.STATUS.b1
        return self.__disk.read(block)

    # Write A Block
    def write_block(self, block, data):
        assert type(block) is int and 1 <= block <= self.__blocks
        assert type(data) is str and len(data) == self.__size
        assert self.__disk.status(block) == self.STATUS.b1
        self.__seed(data)
        self.__disk.write(block, data)

    # Close A Block
    def close_block(self, block):
        assert type(block) is int and 1 <= block <= self.__blocks
        assert self.__disk.status(block) == self.STATUS.b1
        self.__disk.close(block)

    # Get Status Information
    def status(self, block):
        assert type(block) is int and 1 <= block <= self.__blocks
        return self.__disk.status(block)

    # Seed Control Interface
    def seed(self, data=None):
        return self.__seed(data)

    # Probability Of Failure
    def fail(self, probability):
        self.__disk.fail(probability)

    # Dump To File
    def dump(self, name):
        self.__disk.write(0, self.__seed())
        self.__disk.dump(name)

    # Load From File
    def load(self, name, abstract):
        assert type(abstract) is bool
        self.__disk.load(name, abstract)
        self.__blocks, self.__size = self.__disk.info()
        self.__blocks -= 1
        assert 0 < self.__blocks <= self.MAX_BLOCKS
        assert 4 < self.__size <= self.MAX_SIZE
        self.__seed = Seed(self.__disk.read(0))
        if abstract:
            self.__soft()
        else:
            self.__hard()

    # Fix All Errors
    def __soft(self):
        # Not Yet Implemented
        pass

    # Find Any Error
    def __hard(self):
        # Not Yet Implemented
        pass

################################################################################

def test():
    # Not Yet Implemented
    pass

################################################################################

if __name__ == '__main__':
    test()
