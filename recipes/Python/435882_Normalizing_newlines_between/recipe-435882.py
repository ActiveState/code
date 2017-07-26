def _normalize_newlines(string):
    import re
    return re.sub(r'(\r\n|\r|\n)', '\n', string)
