from dal_6 import DAL6, Context
from sys import exit

################################################################################

def main():
    welcome()
    loop()

def welcome():
    print '+---------------------+'
    print '|      DISK DEMO      |'
    print '| by Stephen Chappell |'
    print '+---------------------+'

def loop():
    valid_disk = False
    while True:
        print
        print 'PROGRAM MENU'
        print '============'
        print '(1) Create Disk'
        print '(2) Load Disk'
        if valid_disk:
            print '(3) Save Disk'
            print '(4) Use Disk'
        while True:
            try:
                select = raw_input('Select: ')
            except:
                exit(0)
            try:
                select = int(select)
                if 0 < select < 3 or (2 < select < 5 and valid_disk):
                    break
                else:
                    print 'Select should be between 1 and',
                    if valid_disk:
                        print '4.'
                    else:
                        print '2.'
            except:
                print 'Select should be a number.'
            print
        if select == 1:
            disk = create_disk()
            disk.seed(False)
            valid_disk = True
        elif select == 2:
            disk = load_disk()
            disk.seed(False)
            valid_disk = True
        elif select == 3:
            save_disk(disk)
        else:
            use_disk(disk)

def create_disk():
    while True:
        try:
            print
            print 'CREATE A DISK'
            blocks = int(raw_input('BLOCKS: '))
            size = int(raw_input('SIZE: '))
            return DAL6(blocks, size)
        except:
            print 'INCORRECT VALUE'

def load_disk():
    while True:
        try:
            print
            print 'LOAD A DISK'
            name = raw_input('FILENAME: ')
            disk = DAL6(10, 10)
            disk.load(name, False)
            return disk
        except:
            print 'INVALID FILENAME'

def save_disk(disk):
    while True:
        try:
            print
            print 'SAVE THE DISK'
            name = raw_input('FILENAME: ')
            disk.dump(name)
            break
        except:
            print 'INVALID FILENAME'

################################################################################

def use_disk(disk):
    set_fail_rate(disk)
    context = disk.new_context()
    print
    print 'CREATING A SHELL ...'
    Shell(context)
    print 'EXITING THE SHELL ...'

def set_fail_rate(disk):
    while True:
        try:
            print
            print 'SET DISK FAIL RATE'
            probability = float(raw_input('PROBABILITY: '))
            disk.fail(probability)
            break
        except:
            print '0 <= PROBABILITY <= 1'

################################################################################

class Shell:

    # The Users Interface
    def __init__(self, context):
        assert context.__class__ is Context
        self.__context = context
        self.__commands = ['chdir', 'getcwd', 'listdir', \
                           'mkdir', 'rmdir', 'remove', 'exit']
        self.__programs = ['type', 'edit']
        print 'Welcome to DAL'
        print '=============='
        while True:
            try:
                prompt = raw_input('>>> ')
            except:
                continue
            if prompt == 'help':
                print 'COMMANDS:'
                print '  chdir: change current working directory'
                print '  getcwd: get current working directory'
                print '  listdir: display directory contents'
                print '  mkdir: make a new directory'
                print '  rmdir: remove an old directory'
                print '  remove: remove a file'
                print '  exit: terminates this shell'
                print 'PROGRAMS:'
                print '  type: display the contents of a file'
                print '  edit: create a new file'
            else:
                prompt = prompt.split(' ')
                command = prompt[0]
                path = ' '.join(prompt[1:])
                if command in self.__commands:
                    if command == 'chdir':
                        self.__chdir(path)
                    elif command == 'getcwd':
                        self.__getcwd()
                    elif command == 'listdir':
                        self.__listdir(path)
                    elif command == 'mkdir':
                        self.__mkdir(path)
                    elif command == 'rmdir':
                        self.__rmdir(path)
                    elif command == 'remove':
                        self.__remove(path)
                    else:
                        break
                elif command in self.__programs:
                    if command == 'type':
                        try:
                            Type(self.__context, path)
                        except:
                            print 'Type has crashed.'
                    else:
                        try:
                            Edit(self.__context, path)
                        except:
                            print 'Edit has crashed.'
                else:
                    print repr(command), 'is an unrecognized command or program.'

    # Changes Current Directory
    def __chdir(self, path):
        try:
            if self.__context.exists(path):
                if self.__context.isdir(path):
                    self.__context.chdir(path)
                else:
                    print 'PATH IS NOT A DIRECTORY'
            else:
                print 'PATH DOES NOT EXIST'
        except:
            print 'COULD NOT CHANGE CURRENT WORKING DIRECTORY'

    # Get Current Directory
    def __getcwd(self):
        print self.__context.getcwd()

    # Lists Directory Contents
    def __listdir(self, path):
        try:
            if self.__context.exists(path):
                if self.__context.isdir(path):
                    names = self.__context.listdir(path)
                    for name in names:
                        if len(name) > 40:
                            temp = name[:37] + '...'
                        else:
                            temp = name
                        print temp + ' ' * (41 - len(temp)) + '<>',
                        if path:
                            temp = path + ' ' + name
                        else:
                            temp = name
                        if self.__context.isdir(temp):
                            print 'DIR'
                        else:
                            print 'FILE'
                else:
                    print 'PATH IS NOT A DIRECTORY'
            else:
                print 'PATH DOES NOT EXIST'
        except:
            print 'COULD NOT DISPLAY DIRECTORY CONTENTS'

    # Create New Directory
    def __mkdir(self, path):
        try:
            if self.__context.exists(path):
                if self.__context.isfile(path):
                    print 'NAME IS ALREADY IN USE'
                else:
                    print 'THE DIRECTORY ALREADY EXISTS'
            else:
                self.__context.mkdir(path)
        except:
            print 'DIRECTORY COULD NOT BE CREATED'

    # Remove A Directory
    def __rmdir(self, path):
        try:
            if self.__context.exists(path):
                if self.__context.isdir(path):
                    self.__context.rmdir(path)
                else:
                    print 'PATH IS NOT A DIRECTORY'
            else:
                print 'PATH DOES NOT EXIST'
        except:
            print 'DIRECTORY COULD NOT BE REMOVED'

    # Remove A File
    def __remove(self, path):
        try:
            if self.__context.exists(path):
                if self.__context.isfile(path):
                    self.__context.remove(path)
                else:
                    print 'PATH IS NOT A FILE'
            else:
                print 'PATH DOES NOT EXIST'
        except:
            print 'FILE COULD NOT BE REMOVED'
                         
################################################################################

class Type:

    # Display A File
    def __init__(self, context, path):
        assert context.__class__ is Context
        assert type(path) is str
        try:
            print context.file(path, 'r').read()
        except:
            print 'FILE COULD NOT BE FOUND'

################################################################################

class Edit:

    # Create A File
    def __init__(self, context, path):
        assert context.__class__ is Context
        assert type(path) is str
        while True:
            try:
                option = raw_input('write OR append? ')
                assert option == 'write' or option == 'append'
                break
            except:
                pass
        if option[0] == 'a':
            if context.exists(path):
                if context.isfile(path):
                    self.__menu(context, path, 'a')
                else:
                    print 'PATH IN NOT A FILE'
            else:
                print 'FILE DOES NOT EXIST AND WILL NOT BE CREATED'
        else:
            try:
                if context.exists(path):
                    if context.isfile(path):
                        self.__menu(context, path, 'w')
                    else:
                        print 'PATH IS NOT A FILE'
                else:
                    self.__menu(context, path, 'w')
            except:
                print 'FILE COULD NOT BE CREATED'

    # Display A Menu
    def __menu(self, context, path, mode):
        file_object = context.file(path, mode)
        data = self.__edit()
        file_object.write(data)
        file_object.close(False)

    # Get New Lines
    def __edit(self):
        lines = []
        while True:
            try:
                lines.append(raw_input())
            except:
                break
        return '\n'.join(lines)

################################################################################

if __name__ == '__main__':
    main()
