#####################################################################
# broadcaster.py
#

__all__ = ['Register', 'Broadcast',
            'CurrentSource', 'CurrentTitle', 'CurrentData']

listeners = {}
currentSources = []
currentTitles = []
currentData = []

def Register(listener, arguments=(), source=None, title=None):
    if not listeners.has_key((source, title)):
        listeners[(source, title)] = []

    listeners[(source, title)].append((listener, arguments))

def Broadcast(source, title, data={}):
    currentSources.append(source)
    currentTitles.append(title)
    currentData.append(data)

    listenerList = listeners.get((source, title), [])[:]
    if source != None:
        listenerList += listeners.get((None, title), [])
    if title != None:
        listenerList += listeners.get((source, None), [])

    for listener, arguments in listenerList:
        apply(listener, arguments)

    currentSources.pop()
    currentTitles.pop()
    currentData.pop()

def CurrentSource():
    return currentSources[-1]

def CurrentTitle():
    return currentTitles[-1]

def CurrentData():
    return currentData[-1]


#####################################################################
# broker.py
#

__all__ = ['Register', 'Request',
            'CurrentTitle', 'CurrentData']

providers = {}
currentTitles = []
currentData = []

def Register(title, provider, arguments=()):
    assert not providers.has_key(title)
    providers[title] = (provider, arguments)

def Request(title, data={}):
    currentTitles.append(title)
    currentData.append(data)

    result = apply(apply, providers.get(title))

    currentTitles.pop()
    currentData.pop()

    return result

def CurrentTitle():
    return currentTitles[-1]

def CurrentData():
    return currentData[-1]


#####################################################################
# sample.py
#

from __future__ import nested_scopes

import broadcaster
import broker

class UserSettings:
    def __init__(self):
        self.preferredLanguage = 'English'
        # The use of lambda here provides a simple wrapper around
        # the value being provided. Every time the value is requested
        # the variable will be reevaluated by the lambda function.
        # Note the dependence on nested scopes.
        broker.Register('Preferred Language', lambda: self.preferredLanguage)

        self.preferredSkin = 'Cool Blue Skin'
        broker.Register('Preferred Skin', lambda: self.preferredSkin)

    def ChangePreferredSkinTo(self, preferredSkin):
        self.preferredSkin = preferredSkin
        broadcaster.Broadcast('Preferred Skin', 'Changed')

    def ChangePreferredLanguageTo(self, preferredLanguage):
        self.preferredLanguage = preferredLanguage
        broadcaster.Broadcast('Preferred Language', 'Changed')

def ChangeSkin():
    print 'Changing to', broker.Request('Preferred Skin')

def ChangeLanguage():
    print 'Changing to', broker.Request('Preferred Language')

broadcaster.Register(ChangeSkin, source='Preferred Skin', title='Changed')
broadcaster.Register(ChangeLanguage, source='Preferred Language', title='Changed')

userSettings = UserSettings()
userSettings.ChangePreferredSkinTo('Bright Green Skin')
userSettings.ChangePreferredSkinTo('French')
