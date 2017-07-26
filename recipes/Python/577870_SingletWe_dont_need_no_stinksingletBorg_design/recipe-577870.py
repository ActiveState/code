class Borg:
    __shared_state = {}
    
    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls, *args, **kwargs)
        instance.__dict__ = cls.__shared_state
        return instance
