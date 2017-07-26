def restrictiveApi(klas):
    class newklas:
        def __init__(self, *args):
            self.__inst = apply(klas, args)
        def __getattr__(self, attr):
            # If the attribute is in the permitted API, then return
            # the correct thing, no matter who asks for it.
            #
            if attr in self.__inst._PUBLIC:
                return getattr(self.__inst, attr)
            # If the attribute is outside the permitted API, then
            # return it only if the calling class is in the list of
            # friends. Otherwise raise an AttributeError.
            #
            elif hasattr(self.__inst, '_FRIENDS'):
                # find the class of the method that called us
                try:
                    raise Exception
                except:
                    import sys
                    tb = sys.exc_info()[2]
                    callerClass = tb.tb_frame.f_back.f_locals['self'].__class__
                # if it's a friend class, return the requested thing
                if callerClass.__name__ in self.__inst._FRIENDS:
                    return getattr(self.__inst, attr)
            # if not a friend, raise an AttributeError
            raise AttributeError, attr
    return newklas
