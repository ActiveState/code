# ! /usr/bin/env python
# Lumberjack.py
# Author: D. Haynes
# 9th July 2002
# 
# For more details on mix-ins, see
# http://www.linuxjournal.com/article.php?sid=4540

class CambridgeMan:
    def roots(self):
        return "But I'm forever a Cambridge Man"

class LumberjackInterface:
    def __init__(self, methods):
        self.methods = list(methods)

    def __iter__(self):
        return self

    def next(self):
        try:
            return self.methods.pop(0)
        except IndexError:
            raise StopIteration

class LumberjackBase(CambridgeMan):
    def __init__(self, name):
        self.bases = self.__class__.__bases__
        self.name = name
        self.title = "Young %s" % self.name

    def _mixIn(self, mixInClass):
        self.__class__.__bases__ = (mixInClass,) + self.bases
        mixInClass.__init__(self, self.name)

    def Interface(self):
        """
            Return a list of the names of the methods to be used by
            the client.

        """
        unpublishedMethods = ("roots", "Interface",
        "WishIdBeenAGirlie")
        methodType = type(self.Interface)
        ifList = []
        for i in dir(self):
            if (type(getattr(self, i)) == methodType
            and not i.startswith('_')):
                ifList.append(i)
        for i in unpublishedMethods:
            ifList.remove(i)
        return LumberjackInterface(ifList)

class RookieLumberjackMixIn:
    """
        I cut down trees, I eat my lunch, I go to the lavatory.
        On Wednesdays I go shopping, and have buttered scones for
        tea...

    """

    def __init__(self, name):
        self.name = name
        self.title = "Young %s" % self.name

    def CutDownTrees(self):
        return "%s cut down a tree." % self.name

    def EatMyLunch(self):
        return "%s eats his lunch." % self.name

    def GoShopping(self):
        return "%s has gone shopping." % self.name

    def WishIdBeenAGirlie(self):
        return 0


class SeasonedLumberjackMixIn:
    """
        I cut down trees, I skip and jump, I like to press wild
        flowers. I put on womens' clothing, and hang around in bars...

    """

    def __init__(self, name):
        self.name = name
        self.title = "Head Lumberjack %s" % name

    def CutDownTrees(self):
        return "%s cut down a tree." % self.name

    def SkipAndJump(self):
        return "%s skips and jumps." % self.name

    def HangAroundInBars(self):
        return "%s is in the bar." % self.name

    def WishIdBeenAGirlie(self):
        return 0

class VeteranLumberjackMixIn:
    """
        I cut down trees, I wear high heels, suspenders and a bra.
        I wish I'd been a girlie, just like my dear Papa...

    """
    def __init__(self, name):
        self.name = name
        self.title = "Old Man %s" % name

    def CutDownTrees(self):
        return "%s cut down a tree." % self.name

    def WearHighHeels(self):
        return "%s has stilletos on." % self.name

    def WishIdBeenAGirlie(self):
        return 1

class LumberjackFactory:
    def __init__(self):
        pass

    def Lumberjack(self, name):
        jack = LumberjackBase(name)
        jack._mixIn(RookieLumberjackMixIn)
        return jack

def display(jack):
    print "I'm %s and I can..." % jack.title
    for i in jack.Interface():
        print i
    print "And I do%s wish I was a girlie!" % ("n't" * (1 - jack.
    WishIdBeenAGirlie()))
    print

def do(jack):
    for i in jack.Interface():
        print apply(getattr(jack, i))
    print

if __name__ == "__main__":
    factory = LumberjackFactory()
    jack = factory.Lumberjack("Jack")
    display(jack)
    do(jack)

    jack._mixIn(SeasonedLumberjackMixIn)
    display(jack)
    do(jack)

    jack._mixIn(VeteranLumberjackMixIn)
    display(jack)
    do(jack)

    print jack.roots()
