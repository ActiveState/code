import sys

if sys.version_info[:2] > (2, 2):
    def dequote(string, dictionary):
        """Replace quoted parts of string with dictionary entries."""
        parts = string.split('"')
        parts[1::2] = [dictionary[word] for word in parts[1::2]]
        return ''.join(parts)
else:
    def dequote(string, dictionary):
        """Replace quoted parts of string with dictionary entries."""
        parts = string.split('"')
        for i in range(1, len(parts), 2):
            parts[i] = dictionary[parts[i]]
        return ''.join(parts)
