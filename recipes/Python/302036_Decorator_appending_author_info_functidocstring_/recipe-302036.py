def author(name):
    def setauthor(func):
        author = "Author: %s" % name
        if func.__doc__:
            author += "\n" + func.__doc__
        func.__doc__ = author
        return func
    return setauthor
