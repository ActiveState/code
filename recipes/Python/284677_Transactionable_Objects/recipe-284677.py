class Transaction(object):
    def __init__(self):
        self.__log = []
    def _commit(self):
        self.__log.append(self.__dict__.copy())
    def _rollback(self):
        try:
            self.__dict__.update(self.__log.pop(-1))
        except IndexError:
            pass
            
