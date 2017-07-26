import os, sys

################################################################################

def main():
    try:
        tree = SizeTree(os.path.abspath(sys.argv[1]))
    except IndexError:
        print('Usage: {} <directory>'.format(os.path.basename(sys.argv[0])))
    else:
        show(tree)

def show(tree):
    print('{} [{}]'.format(tree.path, convert(tree.total_size)))
    walk(tree, '')
    if not tree.children:
        print('No subfolders exist')

def walk(tree, prefix):
    dir_prefix, walk_prefix = prefix + '+---', prefix + '|   '
    for pos, neg, child in enumerate2(tree.children):
        if neg == -1:
            dir_prefix, walk_prefix = prefix + '\\---', prefix + '    '
        print('{}{} [{}]'.format(dir_prefix, child.name,
                                 convert(child.total_size)))
        walk(child, walk_prefix)

def enumerate2(sequence):
    length = len(sequence)
    for count, value in enumerate(sequence):
        yield count, count - length, value

################################################################################

class SizeTree:

    def __init__(self, path, name=None):
        self.path = path
        self.name = os.path.basename(path) if name is None else name
        self.children = []
        self.file_size = 0
        self.total_size = 0
        try:
            dir_list = os.listdir(path)
        except OSError:
            pass
        else:
            for name in dir_list:
                path_name = os.path.join(path, name)
                if os.path.isdir(path_name):
                    size_tree = SizeTree(path_name, name)
                    self.children.append(size_tree)
                    self.total_size += size_tree.total_size
                elif os.path.isfile(path_name):
                    try:
                        self.file_size += os.path.getsize(path_name)
                    except OSError:
                        pass
        self.total_size += self.file_size

################################################################################

def convert(number):
    "Convert bytes into human-readable representation."
    if not number:
        return '0 Bytes'
    assert 0 < number < 1 << 110, 'number out of range'
    ordered = reversed(tuple(format_bytes(partition_number(number, 1 << 10))))
    cleaned = ', '.join(item for item in ordered if item[0] != '0')
    return cleaned

def partition_number(number, base):
    "Continually divide number by base until zero."
    div, mod = divmod(number, base)
    yield mod
    while div:
        div, mod = divmod(div, base)
        yield mod

def format_bytes(parts):
    "Format partitioned bytes into human-readable strings."
    for power, number in enumerate(parts):
        yield '{} {}'.format(number, format_suffix(power, number))

def format_suffix(power, number):
    "Compute the suffix for a certain power of bytes."
    return (PREFIX[power] + 'byte').capitalize() + ('s' if number != 1 else '')

PREFIX = ' kilo mega giga tera peta exa zetta yotta bronto geop'.split(' ')

################################################################################

if __name__ == '__main__':
    main()
