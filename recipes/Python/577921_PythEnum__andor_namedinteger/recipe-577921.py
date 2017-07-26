"""Enumeration class representing a named integer."""


class Enum(int):
    """Enumeration value is a named integer."""
    #pylint: disable=R0904

    def __new__(cls, rank, name):
        obj = int.__new__(cls, rank)
        obj.name = name
        return obj

    def __repr__(self):
        return 'Enum(' + repr(int(self)) + ', ' + repr(self.name) + ')'

    @staticmethod
    def lookup(enumvals):
        """Lookup from int/string to Enum instance for provided values"""
        result = {int(v): v for v in enumvals}
        result.update({v.name: v for v in enumvals})
        return result


def test():
    """Tests of the Enum class"""
    # pylint: disable=C0103
    WEAK = Enum(1, 'WEAK')
    MODERATE = Enum(2, 'MODERATE')
    STRONG = Enum(3, 'STRONG')
    assert repr(STRONG) == "Enum(3, 'STRONG')"
    assert WEAK < MODERATE < STRONG
    assert MODERATE > WEAK
    assert WEAK.name == 'WEAK'
    assert WEAK == 1
    assert WEAK < 3

if __name__ == '__main__':
    test()
