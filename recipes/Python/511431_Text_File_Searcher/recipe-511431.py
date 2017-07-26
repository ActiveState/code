import os

def main():
    try:
        directory = get_directory()
        text = get_text()
        results = do_search(directory, text)
        finish(results)
    except:
        pass

def get_directory():
    while True:
        try:
            directory = raw_input('Directory: ')
            assert os.path.isdir(directory)
            return directory
        except AssertionError:
            print 'You must enter a directory.'

def get_text():
    while True:
        try:
            text = raw_input('Text: ').lower()
            assert text
            return text
        except AssertionError:
            print 'You must enter some text.'

def do_search(directory, text):
    results = list()
    for dirpath, dirnames, filenames in os.walk(directory):
        for name in filenames:
            full_path = os.path.join(dirpath, name)
            if text in file(full_path).read().lower():
                results.append(full_path)
    return results

def finish(results):
    print
    for filename in results:
        print filename
    raw_input('Done.')

if __name__ == '__main__':
    main()
