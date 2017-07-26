import disk

################################################################################

class DiskDriver(disk.DiskDriver):

    # Get Configuration Information
    def info(self):
        return self.__blocks, self.__size

################################################################################

class DAL1:

    # DEFAULTS (16 MB)
    BLOCKS = (2 ** 12)
    SIZE = (2 ** 12)

    # Disk Abstraction Layer
    def __init__(self):
        self.__disk = DiskDriver(self.BLOCKS, self.SIZE)
        self.__blocks, self.__size = self.__disk.info()
        self.__end = self.__blocks * self.__size

    # Read Some Data
    def read(self, index, size):
        assert type(index) is int and 0 <= index < self.__end
        assert type(size) is int and index < index + size <= self.__end
        first_index = index
        last_index = index + size - 1
        first_block = first_index / self.__size + 1
        last_block = last_index / self.__size + 2
        stream = ''.join([self.__read(block) for block in \
                          range(first_block, last_block)])
        first_index = index % self.__size
        last_index = first_index + size
        return stream[first_index:last_index]

    # Write Some Data
    def write(self, index, data):
        size = len(data)
        assert type(index) is int and 0 <= index < self.__end
        assert type(data) is str and index < index + size <= self.__end
        first_index = index
        last_index = index + size - 1
        first_block = first_index / self.__size + 1
        last_block = last_index / self.__size + 2
        blocks = last_block - first_block
        if blocks == 1:
            if size == self.__size:
                self.__write(first_block, data)
            else:
                stream = self.__read(first_block)
                first_index = index % self.__size
                last_index = first_index + size
                stream = stream[:first_index] + data + stream[last_index:]
                self.__write(first_block, stream)
        else:
            if index % self.__size:
                stream = self.__read(first_block)
                first_index = index % self.__size
                last_index = self.__size - first_index
                stream = stream[:first_index] + data[:last_index]
                data = data[last_index:]
                self.__write(first_block, stream)
            else:
                last_index = self.__size
                stream = data[:last_index]
                data = data[last_index:]
                self.__write(first_block, stream)
            first_block += 1
            last_block -= 1
            for block in range(first_block, last_block):
                self.__write(block, data[:self.__size])
                data = data[self.__size:]
            size = len(data)
            if size == self.__size:
                self.__write(last_block, data)
            else:
                stream = self.__read(last_block)
                stream = data + stream[size:]
                self.__write(last_block, stream)

    # Erase Some Data
    def erase(self, index, size):
        assert type(index) is int and 0 <= index < self.__end
        assert type(size) is int and index < index + size <= self.__end
        first_index = index
        last_index = index + size - 1
        first_block = first_index / self.__size + 1
        last_block = last_index / self.__size + 2
        blocks = last_block - first_block
        if blocks == 1:
            if size == self.__size:
                self.__erase(first_block)
            else:
                stream = self.__read(first_block)
                first_index = index % self.__size
                last_index = first_index + size
                stream = stream[:first_index] + chr(0) * size + \
                         stream[last_index:]
                self.__write(first_block, stream)
        else:
            if index % self.__size:
                stream = self.__read(first_block)
                first_index = index % self.__size
                last_index = self.__size - first_index
                stream = stream[:first_index] + chr(0) * last_index
                self.__write(first_block, stream)
            else:
                self.__erase(first_block)
            first_block += 1
            last_block -= 1
            for block in range(first_block, last_block):
                self.__erase(block)
            last_index = index + size - 1
            size = (last_index % self.__size) + 1
            if size == self.__size:
                self.__erase(last_block)
            else:
                stream = self.__read(last_block)
                stream = chr(0) * size + stream[size:]
                self.__write(last_block, stream)

    # Probability Of Failure
    def fail(self, probability):
        self.__disk.fail(probability)

    # Dump To File
    def dump(self, name):
        self.__disk.dump(name)

    # Load From File
    def load(self, name):
        self.__disk.load(name)
        self.__blocks, self.__size = self.__disk.info()
        self.__end = self.__blocks * self.__size
        self.BLOCKS, self.SIZE = self.__blocks, self.__size

    # Private Utility Function
    def __read(self, block):
        while True:
            try:
                return self.__disk.read(block)
            except:
                pass

    # Private Utility Function
    def __write(self, block, data):
        while True:
            try:
                return self.__disk.write(block, data)
            except:
                pass

    # Private Utility Function
    def __erase(self, block):
        while True:
            try:
                return self.__disk.erase(block)
            except:
                pass

################################################################################

class Test:

    # DAL1 Test Class
    def __init__(self, size):
        self.__string = chr(0) * size

    # Read Some Data
    def read(self, index, size):
        assert type(index) is int and 0 <= index < len(self)
        assert type(size) is int and index < index + size <= len(self)
        return self.__string[index:index+size]

    # Write Some Data
    def write(self, index, data):
        assert type(index) is int and 0 <= index < len(self)
        assert type(data) is str and index < index + len(data) <= len(self)
        self.__string = self.__string[:index] + data + \
                        self.__string[index+len(data):]

    # Erase Some Data
    def erase(self, index, size):
        self.write(index, chr(0) * size)

    # Get Length Information
    def __len__(self):
        return len(self.__string)

################################################################################

def test():
    from os import urandom
    from random import randint
    BLOCKS = DAL1.BLOCKS = 100
    SIZE = DAL1.SIZE = 100
    test1 = DAL1()
    test2 = Test(BLOCKS * SIZE)
    test1.fail(0.999)
    for temp in range(BLOCKS / 2):
        print 'Write:', temp + 1, '/', BLOCKS / 2
        write = randint(0, (BLOCKS * SIZE) / 2), urandom(randint(1, SIZE * 2))
        test1.write(*write)
        test2.write(*write)
        index = randint((BLOCKS * SIZE) / 2, BLOCKS * SIZE)
        data = urandom(randint(1, SIZE * 2))
        write = index - len(data) + 1, data
        test1.write(*write)
        test2.write(*write)
    for temp in range(BLOCKS / 20):
        print 'Erase:', temp + 1, '/', BLOCKS / 20
        erase = randint(0, (BLOCKS * SIZE) / 2), randint(1, SIZE * 2)
        test1.erase(*erase)
        test2.erase(*erase)
        index = randint((BLOCKS * SIZE) / 2, BLOCKS * SIZE)
        size = randint(1, SIZE * 2)
        erase = index - size + 1, size
        test1.erase(*erase)
        test2.erase(*erase)
    raw_input('Tested To ' + str(test1.read(0, BLOCKS * SIZE) == \
                                 test2.read(0, BLOCKS * SIZE)))

################################################################################

if __name__ == '__main__':
    test()
