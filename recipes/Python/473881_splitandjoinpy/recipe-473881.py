import os               # give access to os.path & os.remove
import md5              # allows md5.md5(arg).digest() for file signature
import time             # gives access to time.sleep
import random           # gives access to random.randrange
import thread           # to start new threads
import cPickle          # to pickle and unpickle the index
import Tkinter          # provides GUI tools
import tkFileDialog     # provides some GUI dialogs

THREAD_FLAG = False                 # we'll use this to control the flag

class Application:                  # this is the main class / [function]
    
    FILE_SIZE = 1024 * 1024         # this is an approximate size of output files
    PART_SIZE = 1024                # this is used to tune the "disguising" engine

    # main class function
    def __init__(self):
        self.__root = Tkinter.Tk()          # open the main window
        self.__root.title('Split & Join')   # give it a name
        self.__root.resizable(False, False) # disable resizing

        # starts the splitter engine
        split = Tkinter.Button(self.__root, text='Split', font='Courier 8', command=self.split)
        split.grid(row=0, column=0, padx=15, pady=5)

        # starts the joiner engine
        join = Tkinter.Button(self.__root, text='Join', font='Courier 8', command=self.join)
        join.grid(row=0, column=1, padx=15, pady=5)

        # used for saving / opening files
        self.__open = tkFileDialog.Open()
        self.__save = tkFileDialog.Directory()

        # don't forget to execute!
        self.__root.mainloop()

    # wrap the splitter engine
    def split(self):
        global THREAD_FLAG
        if not THREAD_FLAG:
            self.__root.withdraw()
            self.__start()
            try:
                self.__do_split()
                self.__stop('SPLIT - DONE')
            except:
                self.__stop('SPLIT - FAIL')
            self.__root.deiconify()
                    
    # wrap the joiner engine
    def join(self):
        global THREAD_FLAG
        if not THREAD_FLAG:
            self.__root.withdraw()
            self.__start()
            try:
                self.__do_join()
                self.__stop('JOIN - DONE')
            except:
                self.__stop('JOIN - FAIL')
            self.__root.deiconify()
            
    # remind the user that the program is working
    def __working(self):
        global THREAD_FLAG
        state, key = 0, ['|', '/', '-', '\\']
        while THREAD_FLAG:
            os.system('cls')
            print '.' * (state / 8) + key[state % 4]
            state += 1
            time.sleep(0.125)

    # start the reminder thread
    def __start(self):
        global THREAD_FLAG
        THREAD_FLAG = True
        thread.start_new_thread(self.__working, ())

    # stop the reminder thread
    def __stop(self, message):
        global THREAD_FLAG
        THREAD_FLAG = False
        time.sleep(0.25)
        os.system('cls')
        print message

    # get the signature of the file specified by path
    def __signature(self, path):
        return md5.md5(file(path, 'rb').read()).digest()

    # split string so len(part) == size
    def __partition(self, string, size):
        if len(string) % size:
            parts = len(string) / size + 1
        else:
            parts = len(string) / size
        return [string[index*size:index*size+size] for index in range(parts)]

    # get a source file and a destination folder
    def __get_source_and_destination(self):
        return open(self.__open.show(), 'rb'), self.__save.show()

    # create a random key
    def __new_key(self):
        data = range(256)
        key = ''
        while data:
            index = random.randrange(len(data))
            key += chr(data[index])
            del data[index]
        return key

    # encode a string
    def __s2c(self, string):
        '''s2c(str string)

        Convert from string to code.'''
        self.__assert_type((str, string))
        return self.__n2c(self.__s2n(string))

    # convert number to code
    def __n2c(self, number):
        self.__assert_type((long, number))
        code = ''
        while number:
            code = chr(number % 255 + 1) + code
            number /= 255
        return code

    # convert string to number
    def __s2n(self, string):
        self.__assert_type((str, string))
        number = 1L
        for character in string:
            number <<= 8
            number += ord(character)
        return number

    # make sure that type checking passes
    def __assert_type(self, *tuples):
        for types, objects in tuples:
            if type(objects) is not types:
                raise TypeError

    # this is the splitter engine
    def __do_split(self):
        # get file and folder
        source, destination = self.__get_source_and_destination()
        # make sure that there is a destination
        assert destination != ''
        # index will be the master file to the many files, key will be for mangling
        index = [os.path.basename(source.name), self.__new_key()]
        # devide the source for the individual files
        data = self.__partition(source.read(), self.FILE_SIZE)
        # all source data has been collected, so close it
        source.close()
        # write the individual files
        for num, part in enumerate(data):
            # figure out what the filename will be
            dest_path = os.path.join(destination, '%s.%s.part' % (num, os.path.basename(source.name)))
            # open the file for writing
            dest_file = open(dest_path, 'wb')
            # mangle part to be indistiguishable
            part = part.translate(index[1])
            # partition part for futher mangling
            part = self.__partition(part, self.PART_SIZE)
            # mangle each part again
            part = [self.__s2c(x) for x in part]
            # write the joined parts after mangling
            dest_file.write(chr(0).join(part).translate(index[1]))
            # close the destination
            dest_file.close()
            # add the signature to index
            index.append(self.__signature(dest_path))
        # write the index
        cPickle.dump(index, file(os.path.join(destination, '%s.part' % os.path.basename(source.name)), 'wb'))

    # return an inverted key
    def __inverse(self, key):
        array = range(256)
        for num, char in enumerate(key):
            array[ord(char)] = chr(num)
        return ''.join(array)

    # verify unpacking
    def __check_index(self, index, dirname, source):
        all_path = list()
        for num, signature in enumerate(index):
            all_path.append(os.path.join(dirname, '%s.%s' % (num, source)))
            present = self.__signature(all_path[-1])
            assert signature == present
        return all_path

    # convert from code to string
    def __c2s(self, code):
        '''c2s(str code)

        Convert from code to string.'''
        self.__assert_type((str, code))
        return self.__n2s(self.__c2n(code))

    # convert from code to number
    def __c2n(self, code):
        self.__assert_type((str, code))
        number = 0L
        for character in code:
            number *= 255
            number += ord(character) - 1
        return number

    # convert from number to string
    def __n2s(self, number):
        self.__assert_type((long, number))
        string = ''
        while number > 1:
            string = chr(number & 0xFF) + string
            number >>= 8
        return string


    # this is the joiner engine
    def __do_join(self):
        # get the source file and destination folder
        source, destination = self.__get_source_and_destination()
        # make sure that there is a destination
        assert destination != ''
        # reload the index
        index = cPickle.load(source)
        # close the source
        source.close()
        # make sure that the name of the source agrees with itself
        assert index[0] == os.path.basename(source.name)[:-5]
        # save the key
        key = index[1]
        # do a mild check of the key
        assert len(key) == 256
        # invert the key for decoding purposes
        key = self.__inverse(key)
        # get the dirname from source
        dirname = os.path.dirname(source.name)
        # verify that all files are present and valid
        all_path = self.__check_index(index[2:], dirname, os.path.basename(source.name))
        # if all files were verfied, they just need to put together now [file]
        dest_file = open(os.path.join(destination, index[0]), 'wb')
        # go through all of the files
        for path in all_path:
            # open the source
            source2 = open(path, 'rb')
            # get the source data
            data = source2.read()
            # close the source
            source2.close()
            # automatically clean up the source
            os.remove(path)
            # translate the data
            data = data.translate(key)
            # get the parts
            parts = data.split(chr(0))
            # decode the parts
            parts = [self.__c2s(part) for part in parts]
            # calculate the string to be written
            final = ''.join(parts).translate(key)
            # write the data
            dest_file.write(final)
        # close the destination
        dest_file.close()
        # cleanup the index
        os.remove(source.name)

if __name__ == '__main__':
    Application()
