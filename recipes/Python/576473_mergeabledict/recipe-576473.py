# mergeable_dict - dict with merge() method.
#
# Author: Jerome Lovy

class mergeable_dict(dict):
    """dict with merge() method."""

    def is_compatible_with(self, other):
        for key in self:
            if key in other and self[key] != other[key]:
                return False
        return True

    def merge(self, other):
        for key in other:
            if key in self:
                if self[key] != other[key]:
                    raise ValueError
            else:
                self[key] = other[key]
        return self

    def __ior__(self, other):
        return self.merge(other)

    def __or__(self, other):
        result = mergeable_dict(self)
        for key in other:
            if key in result:
                if result[key] != other[key]:
                    raise ValueError
            else:
                result[key] = other[key]
        return result
