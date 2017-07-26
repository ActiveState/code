@apply
class __all__(object):
    def __getitem__(self, _):
        raise ImportError("Star imports not supported")
