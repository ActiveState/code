import Zcgi

def main():
    Zcgi.print_plain('string = ' + repr(Zcgi.string) + '\n' +
                     'dictionary = ' + repr(Zcgi.dictionary))

if __name__ == '__main__':
    Zcgi.execute(main, 'cgi')
