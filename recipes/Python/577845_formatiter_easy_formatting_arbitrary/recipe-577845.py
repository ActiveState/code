# Remove the '*, ' keyword-only marker for 2.7 compatibility
# Make the default format string '{0!r}' for 2.6 compatibility
# Default values can obviously be adjusted according to taste

def format_iter(iterable, *, fmt='{!r}', sep=', '):
    """Format and join items in iterable with the given format string and separator"""
    return sep.join(fmt.format(x) for x in iterable)

# Example usage
>>> format_iter(range(10))
'0, 1, 2, 3, 4, 5, 6, 7, 8, 9'
>>> format_iter(range(10), sep='|')
'0|1|2|3|4|5|6|7|8|9'
>>> format_iter(range(10), fmt='{:04b}', sep='|')
'0000|0001|0010|0011|0100|0101|0110|0111|1000|1001'
>>> format_iter(range(10), fmt='{0.real}+{0.imag}j')
'0+0j, 1+0j, 2+0j, 3+0j, 4+0j, 5+0j, 6+0j, 7+0j, 8+0j, 9+0j'
