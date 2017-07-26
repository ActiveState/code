"""
Result of this application:

Is Barney older than Lieschen? -> True!
Is Thomas older than Lieschen? -> True!
Is Thomas older than Barney? -> True!
Is Iris older than Lieschen? -> True!
Is Iris older than Barney? -> True!
Is Thomas older than Iris? -> Not enough information!
Is Iris older than Thomas? -> Not enough information!
Is Lieschen younger than Barney? -> True!
Is Lieschen younger than Iris? -> True!
Is Lieschen younger than Thomas? -> True!
Is Barney younger than Iris? -> True!
Is Barney younger than Thomas? -> True!
Is Thomas younger than Iris? -> Not enough information!
Is Iris younger than Thomas? -> Not enough information!"""
class KnowledgeBase:
    def __init__(self):
        self.antagonism = {}
        self.relationship = {}

    def specialCriteria(self, relationA, relationB):
        """ enuring order of dependency chain: A > B, B > C, ... """
        if relationA[1] == relationB[0]:
            return -1
        if relationA[0] < relationB[0]:
            return -1
        if relationA[0] == relationB[0]:
            if relationA[1] < relationB[1]:
                return -1
            elif relationA[1] > relationB[1]:
                return 1
        return 0

    def defineAntagonism(self, meaning, oppositeMeaning):
        if meaning in self.antagonism or \
           oppositeMeaning in self.antagonism:
           return False

        self.antagonism[meaning] = oppositeMeaning
        return True

    def defineRelationship(self, meaning, nameA, nameB):
        # a register pair meaning/opposite meaning is mandatory
        if not meaning in self.antagonism and \
           not meaning in self.antagonism.values():
           return False

        if not meaning in self.relationship:
            self.relationship[meaning] = [(nameA, nameB)]
        else:
            # is information still available?
            if (nameA, nameB) in self.relationship[meaning]:
                return False
            # you cannot define both: A > B and B > A
            if (nameB, nameA) in self.relationship[meaning]:
                return False

            self.relationship[meaning].append((nameA, nameB))
        # ensure correct order for later search in dependency chain
        self.relationship[meaning].sort(cmp=self.specialCriteria)

        return True

    def indirectQuery(self, nameA, nameB, meaningBase):
        search = nameA
        for key , value in meaningBase:
            if key == search:
                search = value
                if search == nameB:
                    break

        return search == nameB

    def query(self, meaning, nameA, nameB):
        # straight forwared query...
        if meaning in self.relationship:
            meaningBase = self.relationship[meaning]
            # is the information directly stored?
            if (nameA, nameB) in meaningBase:
                return True
            else:
                if self.indirectQuery(nameA, nameB, meaningBase):
                    return True

        # inverse query...
        elif meaning in self.antagonism.values():
            for key, value in self.antagonism.items():
                if value == meaning:
                    meaningBase = self.relationship[key]
                    # is the information directly stored?
                    if (nameB, nameA) in meaningBase:
                        return True
                    else:
                        if self.indirectQuery(nameB, nameA, meaningBase):
                            return True
                    break

        return False

if __name__ == "__main__":
    base = KnowledgeBase()

    assert base.defineAntagonism("older", "younger")

    # trying to store existing information again
    assert not base.defineAntagonism("older", "younger")
    # trying to store existing information again
    assert not base.defineAntagonism("younger", "older")

    assert base.defineRelationship("older", "Iris", "Barney")
    assert base.defineRelationship("older", "Barney", "Lieschen")
    assert base.defineRelationship("older", "Thomas", "Barney")

    # trying to store existing information again
    assert not base.defineRelationship("older", "Iris"  , "Barney")
    # trying to generate inconsistent data. Iris cannot be older and
    # younger than Barney and Barney cannot be older and younger than Iris
    assert not base.defineRelationship("older", "Barney", "Iris")

    testData = \
        [("older",  "Barney",   "Lieschen"), # directly stored \
        ("older",   "Thomas",   "Lieschen"), # directly stored (indirect query) \
        ("older",   "Thomas",   "Barney"),   # directly stored \
        ("older",   "Iris",     "Lieschen"), # directly stored (indirect query) \
        ("older",   "Iris",     "Barney"),   # directly stored \
        ("older",   "Thomas",   "Iris"),     # not defined     \
        ("older",   "Iris",     "Thomas"),   # not defined     \
        ("younger", "Lieschen", "Barney"),   # directly stored (inverse search) \
        ("younger", "Lieschen", "Iris"),     # directly stored (inverser, indirect search) \
        ("younger", "Lieschen", "Thomas"),   # directly stored (inverser, indirect search) \
        ("younger", "Barney",   "Iris"),     # directly stored (inverse search) \
        ("younger", "Barney",   "Thomas"),   # directly stored (inverse search) \
        ("younger", "Thomas",   "Iris"),     # not defined     \
        ("younger", "Iris",     "Thomas")]   # not defined

    for meaning, nameA, nameB in testData:
        result = base.query(meaning, nameA, nameB)

        if result:
            print("Is %s %s than %s? -> True!" % (nameA, meaning, nameB))
        else:
            print("Is %s %s than %s? -> Not enough information!" % (nameA, meaning, nameB))
