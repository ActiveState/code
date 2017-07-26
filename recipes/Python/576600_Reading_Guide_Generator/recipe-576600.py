OLD = ['Genesis', 'Exodus', 'Leviticus', 'Numbers', 'Deuteronomy', 'Joshua',
       'Judges', 'Ruth', '1 Samuel', '2 Samuel', '1 Kings', '2 Kings',
       '1 Chronicles', '2 Chronicles', 'Ezra', 'Nehemiah', 'Esther', 'Job',
       'Psalm', 'Proverbs', 'Ecclesiastes', 'Song of Solomon', 'Isaiah',
       'Jeremiah', 'Lamentations', 'Ezekiel', 'Daniel', 'Hosea', 'Joel',
       'Amos', 'Obadiah', 'Jonah', 'Micah', 'Nahum', 'Habakkuk', 'Zephaniah',
       'Haggai', 'Zechariah', 'Malachi']
NEW = ['Matthew', 'Mark', 'Luke', 'John', 'Acts', 'Romans', '1 Corinthians',
       '2 Corinthians', 'Galatians', 'Ephesians', 'Philippians', 'Colossians',
       '1 Thessalonians', '2 Thessalonians', '1 Timothy', '2 Timothy', 'Titus',
       'Philemon', 'Hebrews', 'James', '1 Peter', '2 Peter', '1 John', '2 John',
       '3 John', 'Jude', 'Revelation']
ALL = OLD + NEW

################################################################################

def main():
    bible_text = get_bible()
    bible_array = parse_bible(bible_text)
    iterator = Bible_Iter(bible_array)
    words = iterator.total / 365
    index = words
    try:
        while True:
            print(iterator.get_reference())
            temp = int(index)
            while temp != iterator.index:
                iterator.next_word()
            iterator.next_vers()
            index += words
    except:
        input('DONE')

def get_bible():
    return open('bible13.txt').read()

def parse_bible(string):
    'Parse Bible and return 3D array.'
    book = chap = vers = 1
    form = '%02u:%03u:%03u'
    book_s, chap_s, vers_s = [], [], []
    start = 0
    while True:
        try:
            start = string.index(form % (book, chap, vers), start) + 11
            end = string.index('\n\n', start)
            vers_s.append(' '.join(string[start:end].split()))
            start = end
            vers += 1
        except:
            if vers != 1:
                chap_s.append(vers_s)
                vers_s = []
                chap += 1
                vers = 1
            elif chap != 1:
                book_s.append(chap_s)
                chap_s = []
                book += 1
                chap = 1
            elif book != 1:
                return book_s
            else:
                raise EOFError

################################################################################

class Bible_Iter:

    def __init__(self, bible_3D):
        self.bible = bible_3D
        self.total = 0
        self.__book = 0
        self.__chap = 0
        self.__vers = 0
        self.__word = 0
        self.index = 0
        for book in bible_3D:
            for chapter in book:
                for index, verse in enumerate(chapter):
                    words = verse.split()
                    chapter[index] = words
                    self.total += len(words)

    def get_word(self):
        return self.bible[self.__book][self.__chap][self.__vers][self.__word]

    def next_word(self):
        self.index += 1
        self.__word += 1
        if len(self.bible[self.__book][self.__chap][self.__vers]) == self.__word:
            self.__word = 0
            self.__vers += 1
            if len(self.bible[self.__book][self.__chap]) == self.__vers:
                self.__vers = 0
                self.__chap += 1
                if len(self.bible[self.__book]) == self.__chap:
                    self.__chap = 0
                    self.__book += 1
                    if len(self.bible) == self.__book:
                        self.__book = 0
                        raise EOFError

    def next_vers(self):
        vers = self.__vers
        while vers == self.__vers:
            self.next_word()

    def get_reference(self):
        book = ALL[self.__book]
        reference = '{0} {1}:{2}'.format(book, self.__chap + 1, self.__vers + 1)
        return reference

################################################################################
    
if __name__ == '__main__':
    main()
