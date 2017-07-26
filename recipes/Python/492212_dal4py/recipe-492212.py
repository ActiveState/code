import dal_3
from math import ceil

################################################################################

class DAL3(dal_3.DAL3):

    # Get Configuration Information
    def info(self):
        return self.__blocks, self.__size

################################################################################

class DAL4:

    # CONSTANTS
    MAX_BLOCKS = (2 ** 16) - 2
    MAX_SIZE = (2 ** 16)
    STATUS = dal_3.enum('closed', 'directory', 'file', 'block')

    # Disk Abstraction Layer
    def __init__(self, blocks, size):
        assert type(blocks) is int and 0 < blocks <= self.MAX_BLOCKS
        assert type(size) is int and 4 < size <= self.MAX_SIZE
        assert int(ceil(float((blocks + 1) * (size + 1)) / size)) \
               <= self.MAX_SIZE
        self.__disk = DAL3(blocks, size)
        self.__blocks, self.__size = self.__disk.info()
        block = self.__disk.open_directory()
        assert block == 1
        self.__disk.write_directory(block, '\x00\x00\x00')

    # Make New Directory
    def make_directory(self, block, name):
        assert type(block) is int and 1 <= block <= self.__blocks
        assert type(name) is str and 1 <= len(name) <= 255
        assert self.status(block) == self.STATUS.directory
        assert self.find(block, name) == 0
        root = self.__disk.read_directory(block)
        new_directory = self.__disk.open_directory()
        root += chr(new_directory >> 8) + chr(new_directory & 0xFF)
        self.__disk.write_directory(block, root)
        data = chr(block >> 8) + chr(block & 0xFF) + chr(len(name)) + name
        self.__disk.write_directory(new_directory, data)
        return new_directory

    # Remove Old Directory
    def remove_directory(self, block):
        assert type(block) is int and 2 <= block <= self.__blocks
        assert self.status(block) == self.STATUS.directory
        assert self.empty(block)
        temp = self.__disk.read_directory(block)
        root = (ord(temp[0]) << 8) + ord(temp[1])
        data = self.__disk.read_directory(root)
        size = ord(data[2])
        header = data[:size+3]
        contents = data[size+3:]
        pointers = [(ord(contents[index*2]) << 8) + ord(contents[index*2+1]) \
                    for index in range(len(contents) / 2)]
        assert block in pointers
        pointers.remove(block)
        assert block not in pointers
        contents = ''.join([chr(pointer >> 8) + chr(pointer & 0xFF) \
                            for pointer in pointers])
        data = header + contents
        self.__disk.write_directory(root, data)
        self.__disk.close_directory(block)
        return root

    # Make New File
    def make_file(self, block, name):
        assert type(block) is int and 1 <= block <= self.__blocks
        assert type(name) is str and 1 <= len(name) <= 255
        assert self.is_directory(block)
        assert not self.exists(block, name)
        root = self.__disk.read_directory(block)
        new_file = self.__disk.open_file()
        root += chr(new_file >> 8) + chr(new_file & 0xFF)
        self.__disk.write_directory(block, root)
        data = chr(block >> 8) + chr(block & 0xFF)
        data += chr(len(name)) + name
        data += '\x00' * 4
        self.__disk.write_file(new_file, data)
        return new_file

    # Remove Old File
    def remove_file(self, block):
        assert type(block) is int and 1 <= block <= self.__blocks
        assert self.is_file(block)
        data = self.__disk.read_file(block)
        size = ord(data[2])
        blocks = data[size+3+4:]
        pointers = [(ord(blocks[index*2]) << 8) + ord(blocks[index*2+1]) \
                    for index in range(len(blocks) / 2)]
        for pointer in pointers:
            self.__disk.close_block(pointer)
        self.__disk.close_file(block)
        root = (ord(data[0]) << 8) + ord(data[1])
        data = self.__disk.read_directory(root)
        size = ord(data[2])
        header = data[:size+3]
        contents = data[size+3:]
        pointers = [(ord(contents[index*2]) << 8) + ord(contents[index*2+1]) \
                    for index in range(len(contents) / 2)]
        assert block in pointers
        pointers.remove(block)
        assert block not in pointers
        contents = ''.join([chr(pointer >> 8) + chr(pointer & 0xFF) \
                            for pointer in pointers])
        data = header + contents
        self.__disk.write_directory(root, data)
        return root

    # Read From File
    def read_file(self, block):
        assert type(block) is int and 1 <= block <= self.__blocks
        assert self.is_file(block)
        data = self.__disk.read_file(block)
        size = ord(data[2])
        stream_length = (ord(data[size+3]) << 24) + (ord(data[size+4]) << 16)
        stream_length += (ord(data[size+5]) << 8) + ord(data[size+6])
        contents = data[size+3+4:]
        pointers = [(ord(contents[index*2]) << 8) + ord(contents[index*2+1]) \
                    for index in range(len(contents) / 2)]
        stream = ''.join([self.__disk.read_block(pointer) \
                          for pointer in pointers])
        return stream[:stream_length]

    # Write To File
    def write_file(self, block, data):
        assert type(block) is int and 1 <= block <= self.__blocks
        assert type(data) is str
        assert self.is_file(block)
        length = len(data)
        file_data = self.__disk.read_file(block)
        size = ord(file_data[2])
        header = file_data[:size+3]
        blocks = file_data[size+3+4:]
        file_map = [(ord(blocks[index*2]) << 8) + ord(blocks[index*2+1]) \
                    for index in range(len(blocks) / 2)]
        if len(data) % self.__size:
            blocks = len(data) / self.__size + 1
        else:
            blocks = len(data) / self.__size
        blocks = [data[index*self.__size:index*self.__size+self.__size] \
                  for index in range(blocks)]
        while len(file_map) > len(blocks):
            self.__disk.close_block(file_map[-1])
            del file_map[-1]
        while len(file_map) < len(blocks):
            file_map.append(self.__disk.open_block())
        if blocks:
            if len(blocks) == 1:
                data = blocks[0]
                data = data + chr(0) * (self.__size - len(data))
                self.__disk.write_block(file_map[0], data)
            else:
                self.__disk.write_block(file_map[0], blocks[0])
                index = 1
                while blocks[index] is not blocks[-1]:
                    self.__disk.write_block(file_map[index], blocks[index])
                    index += 1
                data = blocks[-1]
                data = data + chr(0) * (self.__size - len(data))
                self.__disk.write_block(file_map[-1], data)
        length = chr(length >> 24) + chr((length >> 16) & 0xFF) + \
                 chr((length >> 8) & 0xFF) + chr(length & 0xFF)
        blocks = ''.join([chr(pointer >> 8) + chr(pointer & 0xFF) \
                            for pointer in file_map])
        data = header + length + blocks
        self.__disk.write_file(block, data)
        return block

    # Get Directory Contents
    def list_directory(self, block):
        assert type(block) is int and 1 <= block <= self.__blocks
        assert self.status(block) == self.STATUS.directory
        directory = self.__disk.read_directory(block)
        size = ord(directory[2])
        contents = directory[3+size:]
        pointers = [(ord(contents[index*2]) << 8) + ord(contents[index*2+1]) \
                    for index in range(len(contents) / 2)]
        return pointers

    # Check If Empty
    def empty(self, block):
        assert type(block) is int and 1 <= block <= self.__blocks
        status = self.status(block)
        assert status == self.STATUS.directory or status == self.STATUS.file
        if status == self.STATUS.directory:
            data = self.__disk.read_directory(block)
        else:
            data = self.__disk.read_file(block)
        size = ord(data[2])
        data = data[3+size:]
        if status == self.STATUS.directory:
            return not bool(data)
        else:
            return len(data) == 4

    # Looks For Name
    def find(self, block, name):
        pointers = self.list_directory(block)
        names = [self.name(pointer) for pointer in pointers]
        for block, temp_name in zip(pointers, names):
            if temp_name == name:
                return block
        return 0

    # Returns Directory/File Name
    def name(self, block):
        assert type(block) is int and 1 <= block <= self.__blocks
        status = self.status(block)
        assert status == self.STATUS.directory or status == self.STATUS.file
        if status == self.STATUS.directory:
            data = self.__disk.read_directory(block)
        else:
            data = self.__disk.read_file(block)
        size = ord(data[2])
        name = data[3:3+size]
        return name

    # Changes Directory/File Name
    def rename(self, block, name):
        assert type(block) is int and 2 <= block <= self.__blocks
        assert type(name) is str and 1 <= len(name) <= 255
        status = self.status(block)
        assert status == self.STATUS.directory or status == self.STATUS.file
        if status == self.STATUS.directory:
            data = self.__disk.read_directory(block)
        else:
            data = self.__disk.read_file(block)
        size = ord(data[2])
        root = data[:2]
        contents = data[size+3:]
        new_name = chr(len(name)) + name
        data = root + new_name + contents
        if status == self.STATUS.directory:
            self.__disk.write_directory(block, data)
        else:
            self.__disk.write_file(block, data)
        return block

    # Test For Existance
    def exists(self, block, name):
        return self.find(block, name) != 0

    # Check If File
    def is_file(self, block):
        assert type(block) is int and 1 <= block <= self.__blocks
        return self.status(block) == self.STATUS.file

    # Check If Directory
    def is_directory(self, block):
        assert type(block) is int and 1 <= block <= self.__blocks
        return self.status(block) == self.STATUS.directory

    # Read Block Status
    def status(self, block):
        assert type(block) is int and 1 <= block <= self.__blocks
        status = self.__disk.status(block)
        if status == self.__disk.STATUS.closed:
            return self.STATUS.closed
        elif self.__disk.STATUS.d1 <= status <= self.__disk.STATUS.dZ:
            return self.STATUS.directory
        elif self.__disk.STATUS.f1 <= status <= self.__disk.STATUS.fZ:
            return self.STATUS.file
        else:
            return self.STATUS.block

    # Seed Control Interface
    def seed(self, data=None):
        return self.__disk.seed(data)

    # Probability Of Failure
    def fail(self, probability):
        self.__disk.fail(probability)

    # Dump To File
    def dump(self, name):
        self.__disk.dump(name)

    # Load From File
    def load(self, name, abstract):
        assert type(abstract) is bool
        self.__disk.load(name, abstract)
        self.__blocks, self.__size = self.__disk.info()
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
