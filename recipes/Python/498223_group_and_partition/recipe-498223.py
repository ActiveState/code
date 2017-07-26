### Here is my implementation to partition based on funct's evaluation.
def partition(iterable, func):
    result = {}
    for i in iterable:
        result.setdefault(func(i), []).append(i) 
    return result

### Ian Bicking's Generalized group function
def group(seq):
    '''seq is a sequence of tuple containing (item_to_be_categorized, category)'''
    result = {}
    for item, category in seq:
        result.setdefault(category, []).append(item)
    return result 



########### Usage Example ###############
def is_odd(n):
    return (n%2) == 1

l = range(10)
print partition(l, is_odd)
print group( (item, is_odd(item)) for item in l) 
print group( (item, item%3) for item in l )      # no need for lamda/def


class Article (object):
    def __init__(self, title, summary, author):
        self.title = title
        self.summary = summary
        self.author = author

articles = [ Article('Politics & Me', 'about politics', 'Dave'),
             Article('Fishes & Me', 'about fishes', 'ray'),
             Article('Love & Me', 'about love', 'dave'),
             Article('Spams & Me', 'about spams', 'Ray'), ]

# summaries of articles indexed by author
print group( (article.summary, article.author.lower()) for article in articles )    


########### Output ###############
{False: [0, 2, 4, 6, 8], True: [1, 3, 5, 7, 9]}
{False: [0, 2, 4, 6, 8], True: [1, 3, 5, 7, 9]}
{0: [0, 3, 6, 9], 1: [1, 4, 7], 2: [2, 5, 8]}
{'dave': ['about politics', 'about love'], 'ray': ['about fishes', 'about spams']}
