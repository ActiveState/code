import re
number_pattern = re.compile(r"((\A|(?<=\W))(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?)")

def deciexpr(expr):
    """Substitute Decimals for floats in an expression string.

    >>> from decimal import Decimal
    >>> s = '+21.3e-5*85-.1234/81.6'
    >>> deciexpr(s)
    "+Decimal('21.3e-5')*Decimal('85')-Decimal('.1234')/Decimal('81.6')"

    >>> eval(s)
    0.016592745098039215
    >>> eval(deciexpr(s))
    Decimal("0.01659274509803921568627450980")

    """
    return number_pattern.sub(r"Decimal('\1')", expr)
