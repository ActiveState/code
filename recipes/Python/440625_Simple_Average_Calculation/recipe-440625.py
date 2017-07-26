def main():
    while True:
        try:
            string = raw_input('What numbers should I average? ')
            words = string.split()
            numbers = map(float, words)
            average = sum(numbers) / len(numbers)
            print 'The average is', average
            raw_input('Press enter to quit.\n')
            return
        except:
            print 'ERROR: I can only take numbers!'

if __name__ == '__main__':
    main()
