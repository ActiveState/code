bmp_magic_a = 'BM'
jpg_magic_a = '\xFF\xD8\xFF\xE0'
jpg_magic_z = '\xFF\xD9'

def main():
    welcome()
    while True:
        main_menu()
        if main_query() == 1:
            workspace()
        else:
            print
            break

def welcome():
    print
    print '  Welcome to'
    print 'FILE EXTRACTOR'
    print '=============='
    print

def main_menu():
    print '(1) Open Workspace'
    print '(2) Quit Application'

def main_query():
    while True:
        try:
            select = int(raw_input('Select: '))
            if 0 < select < 3:
                return select
            else:
                print 'ERROR: Selection Must Be 1 Or 2'
        except Exception, error:
            if error.__class__ is EOFError:
                print
            print 'ERROR: Selection Must Be A Number'

def workspace():
    try:
        data = get_file()
        while True:
            work_menu()
            select = work_query()
            if select == 1:
                extract_bmp(data)
            elif select == 2:
                extract_jpg(data)
            elif select == 3:
                break
            else:
                raise SystemExit
    except Exception, error:
        if error.__class__ is SystemExit:
            raise SystemExit
        else:
            print

def get_file():
    while True:
        try:
            return file(raw_input('Filename: '), 'rb', 0).read()
        except Exception, error:
            if error.__class__ is EOFError:
                raise EOFError
            else:
                print 'ERROR: Filename Is Invalid'

def work_menu():
    print '(1) Extract *.BMP'
    print '(2) Extract *.JPG'
    print '(3) Back'
    print '(4) Exit'

def work_query():
    while True:
        try:
            select = int(raw_input('Select: '))
            if 0 < select < 5:
                return select
            else:
                print 'ERROR: Selection Must Be Between 1 And 4'
        except Exception, error:
            if error.__class__ is EOFError:
                print
            print 'ERROR: Selection Must Be A Number'
            
def extract_bmp(data):
    extract(data, True)

def extract_jpg(data):
    extract(data, False)

def extract(data, bmp):
    while True:
        try:
            size = get_size()
            if bmp:
                file_list = search_bmp(data, size)
            else:
                file_list = search_jpg(data, size)
            if len(file_list) == 0:
                print 'ERROR: Cannot Find File'
            else:
                while len(file_list) != 0:
                    print len(file_list), 'files can be extracted.'
                    select = get_select(len(file_list))
                    save_point = get_save_point()
                    save_point.write(file_list[select - 1])
                    save_point.close()
                    del file_list[select - 1]
        except:
            print
            break

def get_size():
    while True:
        try:
            size = int(raw_input('File Size: '))
            if 0 < size < 4294967296:
                return size
            else:
                print 'ERROR: Size Must Be Between 1 And 4294967295'
        except Exception, error:
            if error.__class__ is EOFError:
                raise EOFError
            else:
                print 'ERROR: Size Must Be A Number'

def search_bmp(data, size):
    global bmp_magic_a
    file_list = list()
    search_string = bmp_magic_a \
    + chr((size & 0xFF) >> (8 * 0)) \
    + chr((size & 0xFF00) >> (8 * 1)) \
    + chr((size & 0xFF0000) >> (8 * 2)) \
    + chr((size & 0xFF000000) >> (8 * 3))
    index = data.find(search_string)
    while index != -1:
        file_list.append(data[index:index+size])
        index = data.find(search_string, index + 1)
    while len(file_list) != 0 and len(file_list[-1]) != size:
        del file_list[-1]
    return file_list

def search_jpg(data, size):
    global jpg_magic_a, jpg_magic_z
    file_list = list()
    index_1 = data.find(jpg_magic_a)
    index_2 = data.find(jpg_magic_z, index_1)
    while index_1 != -1 and index_2 != -1:
        if index_2 - index_1 == size - len(jpg_magic_z):
            file_list.append(data[index_1:index_1+size])
        index_1 = data.find(jpg_magic_a, index_1 + 1)
        index_2 = data.find(jpg_magic_z, index_1)
    return file_list

def get_select(numbers):
    while True:
        try:
            select = int(raw_input('Extract: '))
            if 1 <= select <= numbers:
                return select
            else:
                print 'ERROR: Must Be Between 1 And', numbers
        except Exception, error:
            if error.__class__ is EOFError:
                raise EOFError
            else:
                print 'ERROR: Must Be A Number'

def get_save_point():
    while True:
        try:
            return open(raw_input('Save To: '), 'wb', 0)
        except Exception, error:
            if error.__class__ == EOFError:
                raise EOFError
            else:
                print 'ERROR: Filename Is Invalid'

if __name__ == '__main__':
    main()
