def indent(txt, stops=1):
    return '\n'.join(" " * 4 * stops + line for line in  txt.splitlines())
