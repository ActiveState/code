import inspect

def callee():
    return inspect.getouterframes(inspect.currentframe())[1][1:4]

def caller():
    return inspect.getouterframes(inspect.currentframe())[2][1:4]
