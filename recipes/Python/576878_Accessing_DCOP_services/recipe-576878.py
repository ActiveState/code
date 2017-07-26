import pydcop

try:
    # get 'player' service of 'amarok' aplication
    playerService = pydcop.DCOPObject('amarok', 'player')

    # call service methods for getting song information
    info = dict(
        title=playerService.title(),
        artist=playerService.artist(),
        album=playerService.album()
    )

    print '%(artist)s - %(title)s (%(album)s)' % info

except RuntimeError, e:
    print 'Amarok is not running.'

# sample output:
# Mercyful Fate - A Dangerous Meeting (Don't Break The Oath)
