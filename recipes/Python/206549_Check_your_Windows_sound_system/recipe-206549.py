import winsound

try:
    winsound.PlaySound("*", winsound.SND_ALIAS)
    print 'Sound hardware is OK'
except RuntimeError, e:
    print 'Sound hardware has problem,', e
