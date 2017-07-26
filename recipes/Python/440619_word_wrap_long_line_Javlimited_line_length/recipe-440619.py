import string
def wrap(text, width):
    """
    A word-wrap function that preserves existing line breaks
    and most spaces in the text. Expects that existing line
    breaks are posix newlines (\n).

    Inserted newlines will appear with a backslash instead.
    """
    return string.replace(string.replace(string.replace(string.replace(
            string.replace(
             reduce(
                lambda line,
                word,
                width=width: '%s%s%s' %
                  (line,
                   ' \n'[(len(line)-line.rfind('\n')-1 +
                     len(word.split('\n',1)[0]) >= width)],
                   word),
                  string.replace(string.replace(
                                string.replace(text,
                                         ".",
                                         ".___MARK "),
                                 ";",
                                 ";___MARK "),
                        "\n",
                        "___EOL ").split(' ')
                 ),
            "___MARK ", ""),
           "___MARK", ""),
        "\n", "\\\n"),
        "___EOL\\\n", "\n"),
       "___EOL ", "\n")

f=open('MyClass.java', 'r') #REPLACE MyClass.java with filename
msg = ""
for line in f:
        msg = msg+line

print(wrap(msg,70))
