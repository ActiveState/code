from tkinter import *
import traceback
from tkinter.scrolledtext import ScrolledText

CODEC = 'utf8'

# XXX This should import the "markov" module.
# XXX All changes made here should be copied.

################################################################################

class MarkovDemo:

    def __init__(self, master):
        self.prompt_size = Label(master, anchor=W, text='Encode Word Size')
        self.prompt_size.pack(side=TOP, fill=X)

        self.size_entry = Entry(master)
        self.size_entry.insert(0, '8')
        self.size_entry.pack(fill=X)

        self.prompt_plain = Label(master, anchor=W, text='Plaintext Characters')
        self.prompt_plain.pack(side=TOP, fill=X)

        self.plain_entry = Entry(master)
        self.plain_entry.insert(0, '""')
        self.plain_entry.pack(fill=X)

        self.showframe = Frame(master)
        self.showframe.pack(fill=X, anchor=W)

        self.showvar = StringVar(master)
        self.showvar.set("encode")

        self.showfirstradio = Radiobutton(self.showframe,
                                          text="Encode Plaintext",
                                          variable=self.showvar,
                                          value="encode",
                                          command=self.reevaluate)
        self.showfirstradio.pack(side=LEFT)

        self.showallradio = Radiobutton(self.showframe,
                                        text="Decode Cyphertext",
                                        variable=self.showvar,
                                        value="decode",
                                        command=self.reevaluate)
        self.showallradio.pack(side=LEFT)
        
        self.inputbox = ScrolledText(master, width=60, height=10, wrap=WORD)
        self.inputbox.pack(fill=BOTH, expand=1)

        self.dynamic_var = IntVar()
        self.dynamic_box = Checkbutton(master, variable=self.dynamic_var,
                                       text='Dynamic Evaluation',
                                       offvalue=False, onvalue=True,
                                       command=self.reevaluate)
        self.dynamic_box.pack()
                                       
        self.output = Label(master, anchor=W, text="This is your output:")
        self.output.pack(fill=X)
        
        self.outbox = ScrolledText(master, width=60, height=10, wrap=WORD)
        self.outbox.pack(fill=BOTH, expand=1)

        self.inputbox.bind('<Key>', self.reevaluate)

        def select_all(event=None):
            event.widget.tag_add(SEL, 1.0, 'end-1c')
            event.widget.mark_set(INSERT, 1.0)
            event.widget.see(INSERT)
            return 'break'
        self.inputbox.bind('<Control-Key-a>', select_all)
        self.outbox.bind('<Control-Key-a>', select_all)
        self.inputbox.bind('<Control-Key-/>', lambda event: 'break')
        self.outbox.bind('<Control-Key-/>', lambda event: 'break')
        self.outbox.config(state=DISABLED)
        
    def reevaluate(self, event=None):
        if event is not None:
            if event.char == '':
                return
        if self.dynamic_var.get():
            text = self.inputbox.get(1.0, END)[:-1]
            if len(text) < 10:
                return
            text = text.replace('\n \n', '\n\n')
            mode = self.showvar.get()
            assert mode in ('decode', 'encode'), 'Bad mode!'
            if mode == 'encode':
                # Encode Plaintext
                try:
                    # Evaluate the plaintext characters
                    plain = self.plain_entry.get()
                    if plain:
                        PC = eval(self.plain_entry.get())
                    else:
                        PC = ''
                        self.plain_entry.delete(0, END)
                        self.plain_entry.insert(0, '""')
                    # Evaluate the word size
                    size = self.size_entry.get()
                    if size:
                        XD = int(size)
                        while grid_size(text, XD, PC) > 1 << 20:
                            XD -= 1
                    else:
                        XD = 0
                        grid = 0
                        while grid <= 1 << 20:
                            grid = grid_size(text, XD, PC)
                            XD += 1
                        XD -= 1
                    # Correct the size and encode
                    self.size_entry.delete(0, END)
                    self.size_entry.insert(0, str(XD))
                    cyphertext, key, prime = encrypt_str(text, XD, PC)
                except:
                    traceback.print_exc()
                else:
                    buffer = ''
                    for block in key:
                        buffer += repr(block)[2:-1] + '\n'
                    buffer += repr(prime)[2:-1] + '\n\n' + cyphertext
                    self.outbox.config(state=NORMAL)
                    self.outbox.delete(1.0, END)
                    self.outbox.insert(END, buffer)
                    self.outbox.config(state=DISABLED)
            else:
                # Decode Cyphertext
                try:
                    header, cypher = text.split('\n\n', 1)
                    lines = header.split('\n')
                    for index, item in enumerate(lines):
                        try:
                            lines[index] = eval('b"' + item + '"')
                        except:
                            lines[index] = eval("b'" + item + "'")
                    plain = decrypt_str(cypher, tuple(lines[:-1]), lines[-1])
                except:
                    traceback.print_exc()
                else:
                    self.outbox.config(state=NORMAL)
                    self.outbox.delete(1.0, END)
                    self.outbox.insert(END, plain)
                    self.outbox.config(state=DISABLED)
        else:
            text = self.inputbox.get(1.0, END)[:-1]
            text = text.replace('\n \n', '\n\n')
            mode = self.showvar.get()
            assert mode in ('decode', 'encode'), 'Bad mode!'
            if mode == 'encode':
                try:
                    XD = int(self.size_entry.get())
                    PC = eval(self.plain_entry.get())
                    size = grid_size(text, XD, PC)
                    assert size
                except:
                    pass
                else:
                    buffer = 'Grid size will be:\n' + convert(size)
                    self.outbox.config(state=NORMAL)
                    self.outbox.delete(1.0, END)
                    self.outbox.insert(END, buffer)
                    self.outbox.config(state=DISABLED)

################################################################################

import random
CRYPT = random.SystemRandom()

################################################################################

# This section includes functions that
# can test the required key and bootstrap.

# sudoko_key
#  - should be a proper "markov" key
def _check_sudoku_key(sudoku_key):
    # Ensure key is a tuple with more than one item.
    assert isinstance(sudoku_key, tuple), '"sudoku_key" must be a tuple'
    assert len(sudoku_key) > 1, '"sudoku_key" must have more than one item'
    # Test first item.
    item = sudoku_key[0]
    assert isinstance(item, bytes), 'first item must be an instance of bytes'
    assert len(item) > 1, 'first item must have more than one byte'
    assert len(item) == len(set(item)), 'first item must have unique bytes'
    # Test the rest of the key.
    for obj in sudoku_key[1:]:
        assert isinstance(obj, bytes), 'remaining items must be of bytes'
        assert len(obj) == len(item), 'all items must have the same length'
        assert len(obj) == len(set(obj)), \
               'remaining items must have unique bytes'
        assert len(set(item)) == len(set(item).union(set(obj))), \
               'all items must have the same bytes'

# boot_strap
#  - should be a proper "markov" bootstrap
#  - we will call this a "primer"
# sudoko_key
#  - should be a proper "markov" key
def _check_boot_strap(boot_strap, sudoku_key):
    assert isinstance(boot_strap, bytes), '"boot_strap" must be a bytes object'
    assert len(boot_strap) == len(sudoku_key) - 1, \
           '"boot_strap" length must be one less than "sudoku_key" length'
    item = sudoku_key[0]
    assert len(set(item)) == len(set(item).union(set(boot_strap))), \
           '"boot_strap" may only have bytes found in "sudoku_key"'

################################################################################

# This section includes functions capable
# of creating the required key and bootstrap.

# bytes_set should be any collection of bytes
#  - it should be possible to create a set from them
#  - these should be the bytes on which encryption will follow
# word_size
#  - this will be the size of the "markov" chains program uses
#  - this will be the number of dimensions the "grid" will have
#  - one less character will make up bootstrap (or primer)
def make_sudoku_key(bytes_set, word_size):
    key_set = set(bytes_set)
    blocks = []
    for block in range(word_size):
        blocks.append(bytes(CRYPT.sample(key_set, len(key_set))))
    return tuple(blocks)

# sudoko_key
#  - should be a proper "markov" key
def make_boot_strap(sudoku_key):
    block = sudoku_key[0]
    return bytes(CRYPT.choice(block) for byte in range(len(sudoku_key) - 1))

################################################################################

# This section contains functions needed to
# create the multidimensional encryption grid.

# sudoko_key
#  - should be a proper "markov" key
def make_grid(sudoku_key):
    grid = expand_array(sudoku_key[0], sudoku_key[1])
    for block in sudoku_key[2:]:
        grid = expand_array(grid, block)
    return grid

# grid
#  - should be an X dimensional grid from make_grid
# block_size
#  - comes from length of one block in a sudoku_key
def make_decode_grid(grid, block_size):
    cache = []
    for part in range(0, len(grid), block_size):
        old = grid[part:part+block_size]
        new = [None] * block_size
        key = sorted(old)
        for index, byte in enumerate(old):
            new[key.index(byte)] = key[index]
        cache.append(bytes(new))
    return b''.join(cache)

# grid
#  - should be an X dimensional grid from make_grid
# block
#  - should be a block from a sudoku_key
#  - should have same unique bytes as the expanding grid
def expand_array(grid, block):
    cache = []
    grid_size = len(grid)
    block_size = len(block)
    for byte in block:
        index = grid.index(bytes([byte]))
        for part in range(0, grid_size, block_size):
            cache.append(grid[part+index:part+block_size])
            cache.append(grid[part:part+index])
    return b''.join(cache)

################################################################################

# The first three functions can be used to check an encryption
# grid. The eval_index function is used to evaluate a grid cell.

# grid
#  - grid object to be checked
#  - grid should come from the make_grid function
#  - must have unique bytes along each axis
# block_size
#  - comes from length of one block in a sudoku_key
#  - this is the length of one edge along the grid
#  - each axis is this many unit long exactly
# word_size
#  - this is the number of blocks in a sudoku_key
#  - this is the number of dimensions in a grid
#  - this is the length needed to create a needed markon chain
def check_grid(grid, block_size, word_size):
    build_index(grid, block_size, word_size, [])

# create an index to access the grid with
def build_index(grid, block_size, word_size, index):
    for number in range(block_size):
        index.append(number)
        if len(index) == word_size:
            check_cell(grid, block_size, word_size, index)
        else:
            build_index(grid, block_size, word_size, index)
        index.pop()

# compares the contents of a cell along each grid axis
def check_cell(grid, block_size, word_size, index):
    master = eval_index(grid, block_size, index)
    for axis in range(word_size):
        for value in range(block_size):
            if index[axis] != value:
                copy = list(index)
                copy[axis] = value
                slave = eval_index(grid, block_size, copy)
                assert slave != master, 'Cell not unique along axis!'

# grid
#  - grid object to be accessed and evaluated
#  - grid should come from the make_grid function
#  - must have unique bytes along each axis
# block_size
#  - comes from length of one block in a sudoku_key
#  - this is the length of one edge along the grid
#  - each axis is this many unit long exactly
# index
#  - list of coordinates to access the grid
#  - should be of length word_size
#  - should be of length equal to number of dimensions in the grid
def eval_index(grid, block_size, index):
    offset = 0
    for power, value in enumerate(reversed(index)):
        offset += value * block_size ** power
    return grid[int(offset)]

################################################################################

# The following functions act as a suite that can ultimately
# encrpyt strings, though other functions can be built from them.

# bytes_obj
#  - the bytes to encode
# byte_map
#  - byte tranform map for inserting into the index
# grid
#  - X dimensional grid used to evaluate markov chains
# index
#  - list that starts the index for accessing grid (primer)
#  - it should be of length word_size - 1
# block_size
#  - length of each edge in a grid
def _encode(bytes_obj, byte_map, grid, index, block_size):
    cache = bytes()
    index = [0] + index
    for byte in bytes_obj:
        if byte in byte_map:
            index.append(byte_map[byte])
            index = index[1:]
            cache += bytes([eval_index(grid, block_size, index)])
        else:
            cache += bytes([byte])
    return cache, index[1:]

# bytes_obj
#  - the bytes to encode
# sudoko_key
#  - should be a proper "markov" key
#  - this key will be automatically checked for correctness
# boot_strap
#  - should be a proper "markov" bootstrap
def encrypt(bytes_obj, sudoku_key, boot_strap):
    _check_sudoku_key(sudoku_key)
    _check_boot_strap(boot_strap, sudoku_key)
    # make byte_map
    array = sorted(sudoku_key[0])
    byte_map = dict((byte, value) for value, byte in enumerate(array))
    # create two more arguments for encode
    grid = make_grid(sudoku_key)
    index = list(map(byte_map.__getitem__, boot_strap))
    # run the actual encoding algorithm and create reversed map
    code, index = _encode(bytes_obj, byte_map, grid, index, len(sudoku_key[0]))
    rev_map = dict(reversed(item) for item in byte_map.items())
    # fix the boot_strap and return the results
    boot_strap = bytes(rev_map[number] for number in index)
    return code, boot_strap

# string
#  - should be the string that you want encoded
# word_size
#  - length you want the markov chains to be of
# plain_chars
#  - characters that you do not want to encrypt
def encrypt_str(string, word_size, plain_chars=''):
    byte_obj = string.encode(CODEC, 'ignore')
    encode_on = set(byte_obj).difference(set(plain_chars.encode()))
    sudoku_key = make_sudoku_key(encode_on, word_size)
    boot_strap = make_boot_strap(sudoku_key)
    cyphertext = encrypt(byte_obj, sudoku_key, boot_strap)[0]
    # return encrypted string, key, and original bootstrap
    return cyphertext.decode(CODEC, 'ignore'), sudoku_key, boot_strap

def grid_size(string, word_size, plain_chars):
    encode_on = set(string.encode()).difference(set(plain_chars.encode()))
    return len(encode_on) ** word_size

################################################################################

# The following functions act as a suite that can ultimately
# decrpyt strings, though other functions can be built from them.

# bytes_obj
#  - the bytes to encode
# byte_map
#  - byte tranform map for inserting into the index
# grid
#  - X dimensional grid used to evaluate markov chains
# index
#  - list that starts the index for accessing grid (primer)
#  - it should be of length word_size - 1
# block_size
#  - length of each edge in a grid
def _decode(bytes_obj, byte_map, grid, index, block_size):
    cache = bytes()
    index = [0] + index
    for byte in bytes_obj:
        if byte in byte_map:
            index.append(byte_map[byte])
            index = index[1:]
            decoded = eval_index(grid, block_size, index)
            index[-1] = byte_map[decoded]
            cache += bytes([decoded])
        else:
            cache += bytes([byte])
    return cache, index[1:]

# bytes_obj
#  - the bytes to decode
# sudoko_key
#  - should be a proper "markov" key
#  - this key will be automatically checked for correctness
# boot_strap
#  - should be a proper "markov" bootstrap
def decrypt(bytes_obj, sudoku_key, boot_strap):
    _check_sudoku_key(sudoku_key)
    _check_boot_strap(boot_strap, sudoku_key)
    # make byte_map
    array = sorted(sudoku_key[0])
    byte_map = dict((byte, value) for value, byte in enumerate(array))
    # create two more arguments for decode
    grid = make_grid(sudoku_key)
    grid = make_decode_grid(grid, len(sudoku_key[0]))
    index = list(map(byte_map.__getitem__, boot_strap))
    # run the actual decoding algorithm and create reversed map
    code, index = _decode(bytes_obj, byte_map, grid, index, len(sudoku_key[0]))
    rev_map = dict(reversed(item) for item in byte_map.items())
    # fix the boot_strap and return the results
    boot_strap = bytes(rev_map[number] for number in index)
    return code, boot_strap

# string
#  - should be the string that you want decoded
# word_size
#  - length you want the markov chains to be of
# plain_chars
#  - characters that you do not want to encrypt
def decrypt_str(string, sudoku_key, boot_strap):
    byte_obj = string.encode(CODEC, 'ignore')
    plaintext = decrypt(byte_obj, sudoku_key, boot_strap)[0]
    # return encrypted string, key, and original bootstrap
    return plaintext.decode(CODEC, 'ignore')

################################################################################

def convert(number):
    "Convert bytes into human-readable representation."
    assert 0 < number < 1 << 110, 'Number Out Of Range'
    ordered = reversed(tuple(format_bytes(partition_number(number, 1 << 10))))
    cleaned = ', '.join(item for item in ordered if item[0] != '0')
    return cleaned

################################################################################

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

################################################################################

PREFIX = ' kilo mega giga tera peta exa zetta yotta bronto geop'.split(' ')

################################################################################

if __name__ == '__main__':
    root = Tk()
    root.title('Markov Demo 1')
    demo = MarkovDemo(root)
    root.mainloop()
