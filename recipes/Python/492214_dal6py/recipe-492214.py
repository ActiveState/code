from dal_5 import DAL5

################################################################################

class DAL6:

    # Disk Abstraction Layer
    def __init__(self, blocks, size):
        self.__disk = DAL5(blocks, size)
        
    # Get Context Object
    def new_context(self):
        return Context(self.__disk)

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

################################################################################

class Context:

    # DEFAULTS
    BACK = '..'
    RELATIVE = '.'

    # Relative Path Context
    def __init__(self, disk_object):
        assert disk_object.__class__ is DAL5
        self.__disk = disk_object
        self.__cwd = ''

    # Change Currect Directory
    def chdir(self, path):
        path = self.__resolve_path(path)
        assert self.__disk.is_directory(path)
        self.__cwd = path

    # Get Current Directory
    def getcwd(self):
        return self.__cwd

    # List Directory Contents
    def listdir(self, path):
        path = self.__resolve_path(path)
        assert self.__disk.is_directory(path)
        return self.__disk.list_directory(path)

    # Make New Directory
    def mkdir(self, path):
        path = self.__resolve_path(path)
        assert not self.__disk.exists(path)
        self.__disk.make_directory(path)

    # Remove Old Directory
    def rmdir(self, path):
        path = self.__resolve_path(path)
        assert self.__disk.is_directory(path)
        self.__disk.remove_directory(path)

    # Open A File
    def file(self, path, mode):
        path = self.__resolve_path(path)
        return File(self.__disk, path, mode)

    # Remove A File
    def remove(self, path):
        path = self.__resolve_path(path)
        assert self.__disk.is_file(path)
        self.__disk.remove_file(path)

    # Test For Existance
    def exists(self, path):
        assert type(path) is str
        if path:
            try:
                path = self.__resolve_path(path)
                if path:
                    return self.__disk.exists(path)
                else:
                    return True
            except:
                return False
        return True
        
    # Check If File
    def isfile(self, path):
        path = self.__resolve_path(path)
        return self.__disk.is_file(path)

    # Check If Directory
    def isdir(self, path):
        path = self.__resolve_path(path)
        return self.__disk.is_directory(path)

    # Private Utility Function
    def __resolve_path(self, path):
        assert type(path) is str
        parts = path.split(self.__disk.PATH_SEPARATOR)
        if parts[0] == self.RELATIVE:
            if len(parts) == 1:
                return self.__cwd
            for part in parts[1:]:
                assert part != self.BACK and part != self.RELATIVE
            path = self.__disk.PATH_SEPARATOR.join(parts[1:])
            if self.__cwd:
                return self.__cwd + self.__disk.PATH_SEPARATOR + path
            else:
                return path
        elif parts[0] == self.BACK:
            assert self.__cwd
            if len(parts) == 1:
                cwd_parts = self.__cwd.split(self.__disk.PATH_SEPARATOR)
                del cwd_parts[-1]
                if cwd_parts:
                    return self.__disk.PATH_SEPARATOR.join(cwd_parts)
                else:
                    return ''
            else:
                cwd_parts = self.__cwd.split(self.__disk.PATH_SEPARATOR)
                del cwd_parts[-1]
                index = 1
                while index != len(parts) and parts[index] == self.BACK:
                    del cwd_parts[-1]
                    index += 1
                parts = parts[index:]
                for part in parts:
                    assert path != self.BACK and part != self.RELATIVE
                path = cwd_parts + parts
                if path:
                    return self.__disk.PATH_SEPARATOR.join(path)
                else:
                    return ''
        else:
            return path

################################################################################

class File:

    # MODES
    READ = 'r'
    WRITE = 'w'
    APPEND = 'a'

    # File Accessor Object
    def __init__(self, disk_object, path, mode):
        assert disk_object.__class__ is DAL5
        assert type(path) is str and path
        assert mode == self.READ or mode == self.WRITE or mode == self.APPEND
        self.__disk = disk_object
        if self.__disk.exists(path):
            assert self.__disk.is_file(path)
        else:
            assert mode == self.WRITE
            self.__disk.make_file(path)
        parts = path.split(self.__disk.PATH_SEPARATOR)
        self.closed = self.__closed = False
        self.mode = self.__mode = mode
        self.name = self.__name = parts[-1]
        self.path = self.__path = path
        if mode == self.WRITE:
            self.__stream = ''
        else:
            self.__stream = self.__disk.read_file(path)
        if mode == self.APPEND:
            self.__pointer = len(self.__stream)
        else:
            self.__pointer = 0

    # Permanently Close File
    def close(self, force):
        assert not self.__closed
        success = True
        if self.__disk.exists(self.__path):
            self.__disk.write_file(self.__path, self.__stream)
        else:
            if force:
                try:
                    self.__disk.make_file(self.__path)
                    self.__disk.write_file(self.__path, self.__stream)
                except:
                    success = False
            else:
                success = False
        self.closed = self.__closed = True
        return success

    # Read From File
    def read(self, size=None):
        assert not self.__closed
        assert self.__mode == self.READ
        if size is None:
            size = (2 ** 31) - 1
        else:
            assert type(size) is int and size > 0
        data = self.__stream[self.__pointer:self.__pointer+size]
        pointer = self.__pointer + size
        if pointer > len(self.__stream):
            pointer = len(self.__stream)
        self.__pointer = pointer
        return data

    # Change Pointer Value
    def seek(self, offset, from_start=False):
        assert type(offset) is int
        assert type(from_start) is bool
        assert not self.__closed
        assert self.__mode != self.APPEND
        if from_start:
            assert 0 <= offset <= len(self.__stream)
            self.__pointer = offset
        else:
            pointer = self.__pointer + offset
            assert 0 <= pointer <= len(self.__stream)
            self.__pointer = pointer

    # Return Pointer Value
    def tell(self):
        return self.__pointer

    # Truncate This File
    def truncate(self, size=None):
        assert not self.__closed
        assert self.__mode == self.WRITE
        if size is None:
            self.__stream = self.__stream[:self.__pointer]
        else:
            assert type(size) is int and size >= 0
            self.__stream = self.__stream[:size]
            if self.__pointer > len(self.__stream):
                self.__pointer = len(self.__stream)

    # Write To File
    def write(self, string):
        assert type(string) is str
        assert not self.__closed
        assert self.__mode != self.READ
        head = self.__stream[:self.__pointer]
        tail = self.__stream[self.__pointer+len(string):]
        self.__stream = head + string + tail
        self.__pointer += len(string)

    # Write All Lines
    def writelines(self, sequence, separator=None):
        assert type(sequence) is list
        if separator is None:
            for line in sequence:
                self.write(line)
        else:
            assert type(separator) is str
            self.write(separator.join(sequence))

    # Return File Size
    def size(self):
        return len(self.__stream)

################################################################################

def test():
    # Not Yet Implemented
    pass

################################################################################

if __name__ == '__main__':
    test()
