import os, time

def main():
    status, key = 0, ['|', '/', '-', '\\']
    while True:
        os.system('cls')
        print '.' * (status / 8) + key[status % 4]
        status += 1
        time.sleep(0.1)

if __name__ == '__main__':
    main()
