"""
The dict built-in function has many ways to build dictionaries but it cannot handle a sequence with alternating key and value pairs.

In python 2.3 it can be easily solved by combining dict, zip and extended slices.
"""

def DictFromList(myList):
    return dict(zip(myList[:-1:2], myList[1::2]))

if __name__ == "__main__":
    print DictFromList(["one", 1, "two", 2, "three", 3])
    # prints: {'three': 3, 'two': 2, 'one': 1}

  
