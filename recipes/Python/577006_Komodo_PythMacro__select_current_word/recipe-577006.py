import komodo

scimoz = komodo.editor
word_start = scimoz.wordStartPosition(scimoz.currentPos, True)
word_end = scimoz.wordEndPosition(scimoz.currentPos, True)
scimoz.anchor = word_start
scimoz.currentPos = word_end
