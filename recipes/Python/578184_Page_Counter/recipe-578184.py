import cPickle
import Zcgi

def main():
    try:
        count = cPickle.load(file('count.txt'))
    except:
        count = 0
    count += 1
    cPickle.dump(count, file('count.txt', 'w'))
    Zcgi.print_plain(str(count))

if __name__ == '__main__':
    Zcgi.execute(main, 'cgi')
