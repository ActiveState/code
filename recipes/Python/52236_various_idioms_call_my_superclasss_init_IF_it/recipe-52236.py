class LookBeforeYouLeap(X):
    "look before you leap idiom for call-if-exists"
    def __init__(self):
        if hasattr(X, '__init__'):
            X.__init__(self)
        # subclass-specific initialization follows

class EasierToAskForgiveness1(X):
    "easier to ask forgiveness idiom for call-if-exists"
    # simpler variant
    def __init__(self):
        try: X.__init__(self)
        except AttributeError: pass
        # subclass-specific initialization follows

class EasierToAskForgiveness2(X):
    "easier to ask forgiveness idiom for call-if-exists"
    # more-robust variant
    def __init__(self):
        try: fun = getattr(X, '__init__')
        except AttributeError: pass
        else: fun(self)
        # subclass-specific initialization follows

class HomogeneizeDifferentCases1(X):
    "let's homogeinize different cases idiom for call-if-exists"
    # function-variant
    def __init__(self):
        def doNothing(obj): pass
        fun = getattr(X, '__init__', doNothing)
        fun(self)
        # subclass-specific initialization follows

class HomogeneizeDifferentCases2(X):
    "let's homogeinize different cases idiom for call-if-exists"
    # lambda-variant
    def __init__(self):
        fun = getattr(X, '__init__', lambda x: None)
        fun(self)
        # subclass-specific initialization follows
