from pickle import Pickler, Unpickler   # for saving and loading keys
from random import randint, seed        # for generating keys
from time import time                   # for randomizing keys

def main():
    '''Executes program.

    Shows welcome and menu.
    Gets selection.
    Executes correct part of the program.'''
    show_heading('Welcome to CRYPT')
    print
    exit = False
    while not exit:
        answer = menu()
        if answer is 1:
            create_key()
        elif answer is 2:
            encode_file()
        elif answer is 3:
            decode_file()
        elif answer is 4:
            exit = True
        else:
            raise bug

def show_heading(heading):
    '''Displays headings.

    Prints a heading.
    Underlines the heading.'''
    print heading
    underline = ''
    for line in range(len(heading)):
        underline += '-'
    print underline

def menu():
    '''Handles menu.

    Shows the menu.
    Get and returns a selection.'''
    show_menu()
    return get_answer()

def show_menu():
    '''Displays menu.

    Shows the heading.
    Prints out all selections from the menu.'''
    show_heading('MENU')
    print '(1) Create Key'
    print '(2) Encode File'
    print '(3) Decode File'
    print '(4) Exit Program'
    print

def get_answer():
    '''Receives selection.

    Gets an answer.
    Handles errors.
    Returns answer.'''
    while True:
        try:
            answer = int(raw_input('Please make a selection: '))
            if answer is 1 or answer is 2 or answer is 3 or answer is 4:
                print
                return answer
        except:
            pass
        print 'You must enter 1, 2, 3, or 4 as a selection.'

def create_key():
    '''Generates a key.

    Shows the heading.
    Gets a destination file.
    Creates a key.
    Saves the key in the file.
    Flush the buffer.
    Closes the file.
    Prints confirmation.'''
    show_heading('CREATE KEY')
    key_file = get_destination('What will be the name of the key file?')
    key_data = create_key_data()
    Pickler(key_file).dump(key_data)
    key_file.flush()
    key_file.close()
    print 'The key has been created at the location specified.'
    print

def get_destination(prompt):
    '''Gets destination file.

    Prompts for filename.
    Handles errors.
    Returns file.'''
    while True:
        try:
            key = file(raw_input(prompt + ' '), 'wb')
            return key
        except:
            print 'Please enter a different filename.'

def create_key_data():
    '''Creates a key.

    Generates to lists.
    Creates an area for the key.
    Randomizes the random system.
    Loops 265 times doing the following:
        Creates two different indexs valid for list_one and list_two.
        Creates a tuple of two different and unique numbers.
        Deletes the two number from the two lists.
    Returns the key.'''
    list_one = range(256)
    list_two = range(256)
    key = []
    seed(time())
    for index in range(256):
        index_one = randint(0, 255 - index)
        index_two = randint(0, 255 - index)
        key.append((list_one[index_one], list_two[index_two]))
        del list_one[index_one], list_two[index_two]
    return key

def encode_file():
    '''Executes decoding subsection.

    Shows the heading of this area.
    Gets the source file for encoding.
    Gets the destination file.
    Handles errors.
    Gets a key.
    Executes the main encoding system.
    Prints a confirmation.'''
    show_heading('ENCODE FILE')
    source = get_source('What is the name of the source file?')
    destination = get_destination('What will be the name of the destination file?')
    bad_key = True
    while bad_key:
        try:
            key = get_key()
            work_encode(source, destination, key)
            bad_key = False
        except:
            print 'Please enter a different filename.'
    print 'The encoded file has been created at the location specified.'
    print

def get_source(prompt):
    '''Gets a source file.

    Gets the file.
    Handles errors.
    Returns the file.'''
    while True:
        try:
            source = file(raw_input(prompt + ' '), 'rb')
            return source
        except:
            pass
        print 'Please enter a different filename.'

def get_key():
    '''Gets key data.

    Gets the source of the key.
    Loads the data of the key.
    Closes the key file.
    Returns the key.'''
    key_file = get_source('What is the name of the key file?')
    key = Unpickler(key_file).load()
    key_file.close()
    return key

def work_encode(source, destination, key):
    '''Encodes and saves a file.

    Creates buffers for a new file and a "quick key."
    Generates the "quick key."
    Encodes the old file onto the new file buffer.
    Writes the buffer to the destination.
    Closes the open files.'''
    new_file = ''
    encode_key = range(256)
    for index in range(256):
        encode_key[key[index][0]] = key[index][1]
    for line in source:
        for byte in line:
            new_file += chr(encode_key[ord(byte)])
    destination.write(new_file)
    source.close()
    destination.flush()
    destination.close()

def decode_file():
    '''Decodes a file.

    Shows the heading.
    Gets the source file.
    Gets the destination file.
    Handles errors.
    Gets a key.
    Does the decoding.
    Prints a confirmation.'''
    show_heading('DECODE FILE')
    source = get_source('What is the name of the source file?')
    destination = get_destination('What will be the name of the destination file?')
    bad_key = True
    while bad_key:
        try:
            key = get_key()
            work_decode(source, destination, key)
            bad_key = False
        except:
            print 'Please enter a different filename.'
    print 'The decoded file has been created at the location specified.'
    print

def work_decode(source, destination, key):
    '''Does decoding.

    Creates buffers.
    Generates "quick key."
    Decodes source to buffer.
    Writes buffer to destination.
    Closes files.'''
    new_file = ''
    decode_key = range(256)
    for index in range(256):
        decode_key[key[index][1]] = key[index][0]
    for line in source:
        for byte in line:
            new_file += chr(decode_key[ord(byte)])
    destination.write(new_file)
    source.close()
    destination.flush()
    destination.close()

class bug:                              # for custom exceptions
    pass

if __name__ == '__main__':              # for executing if needed
    main()
