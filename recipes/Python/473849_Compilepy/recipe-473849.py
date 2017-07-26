import os, time

def main():
    master = dict()
    for name in os.listdir(os.getcwd()):
        try:
            master[time.mktime(time.strptime(name, '%A, %B %d, %Y.txt'))] = name
        except:
            pass
    file('Logbook.txt', 'w').write('\n'.join([file(master[index]).read() for index in sorted(master)]))

if __name__ == '__main__':
    main()
