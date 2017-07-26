from dal_4 import DAL4

################################################################################

class DAL5:

    # DEFAULTS
    PATH_SEPARATOR = ' '
    NAME_CHARACTERS = ''.join([chr(i) for i in range(256) \
                               if len(repr(chr(i))) == 3])

    # Disk Abstraction Layer
    def __init__(self, blocks, size):
        self.__disk = DAL4(blocks, size)

    # Make New Directory
    def make_directory(self, path):
        block, name = self.__resolve_path(path)
        self.__disk.make_directory(block, name)

    # Remove Old Directory
    def remove_directory(self, path):
        block, name = self.__resolve_path(path)
        block = self.__disk.find(block, name)
        assert block
        assert self.__disk.is_directory(block)
        assert self.__disk.empty(block)
        self.__disk.remove_directory(block)

    # Make New File
    def make_file(self, path):
        block, name = self.__resolve_path(path)
        self.__disk.make_file(block, name)

    # Remove Old File
    def remove_file(self, path):
        block, name = self.__resolve_path(path)
        block = self.__disk.find(block, name)
        assert block
        assert self.__disk.is_file(block)
        self.__disk.remove_file(block)

    # Read From File
    def read_file(self, path):
        block, name = self.__resolve_path(path)
        block = self.__disk.find(block, name)
        assert block
        return self.__disk.read_file(block)

    # Write To File
    def write_file(self, path, data):
        block, name = self.__resolve_path(path)
        block = self.__disk.find(block, name)
        assert block
        self.__disk.write_file(block, data)

    # Get Directory Contents
    def list_directory(self, path):
        if path:
            block, name = self.__resolve_path(path)
            block = self.__disk.find(block, name)
            assert block
        else:
            block = 1
        directory = self.__disk.list_directory(block)
        names = [self.__disk.name(block) for block in directory]
        return names

    # Check If Empty
    def empty(self, path):
        block, name = self.__resolve_path(path)
        block = self.__disk.find(block, name)
        assert block
        return self.__disk.empty(block)

    # Changes Directory/File Name
    def rename(self, path, name):
        block, old_name = self.__resolve_path(path)
        block = self.__disk.find(block, old_name)
        assert block
        self.__disk.rename(block, name)

    # Test For Existance
    def exists(self, path):
        try:
            block, name = self.__resolve_path(path)
            block = self.__disk.find(block, name)
            assert block
            return True
        except:
            return False

    # Check If File
    def is_file(self, path):
        block, name = self.__resolve_path(path)
        block = self.__disk.find(block, name)
        return self.__disk.is_file(block)

    # Check If Directory
    def is_directory(self, path):
        assert type(path) is str
        if path:
            block, name = self.__resolve_path(path)
            block = self.__disk.find(block, name)
            return self.__disk.is_directory(block)
        else:
            return True

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

    # Private Utility Function
    def __resolve_path(self, path):
        assert type(path) is str
        if path:
            table = ''.join([chr(i) for i in range(256)])
            parts = path.split(self.PATH_SEPARATOR)
            block = 1
            for name in parts[:-1]:
                assert len(name.translate(table, self.NAME_CHARACTERS)) == 0
                block = self.__disk.find(block, name)
                assert block
            assert parts[-1]
            assert len(parts[-1].translate(table, self.NAME_CHARACTERS)) == 0
            return block, parts[-1]
        else:
            return 1, ''

################################################################################

def test():
    # Not Yet Implemented
    pass

################################################################################

if __name__ == '__main__':
    test()
