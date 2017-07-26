# Constants defining the neuron's response curve

minact, rest, thresh, decay, maxact = -0.2, -0.1, 0.0, 0.1, 1.0
alpha, gamma, estr = 0.1, 0.1, 0.4

units = []
pools = []
unitbyname = {}

class Unit(object):
    __slots__ = ['name', 'pool', 'extinp', 'activation', 'output', 'exciters', 'newact']
    def __init__(self, name, pool):
        self.name = name
        self.pool = pool
        self.reset()
        self.exciters = []
        unitbyname[name] = self
    def reset(self):
        self.setext(0.0)
        self._setactivation()
    def setext(self, weight=1.0):
        self.extinp = weight
    def _setactivation(self, val=rest):
        self.activation = val
        self.output = max(thresh, val)
    def addexciter(self, aunit):
        self.exciters.append(aunit)
    def remove(self, aunit):
        self.exciters.remove(aunit)
    def computenewact(self):
        ai = self.activation
        plus = sum(exciter.output for exciter in self.exciters)
        minus = self.pool.sum - self.output
        netinput = alpha*plus - gamma*minus + estr*self.extinp
        if netinput > 0:
            ai = (maxact-ai)*netinput - decay*(ai-rest) + ai
        else:
            ai = (ai-minact)*netinput - decay*(ai-rest) + ai
        self.newact = max(min(ai, maxact), minact)
    def commitnewact(self):
        self._setactivation(self.newact)

class Pool(object):
    __slots__ = ['sum', 'members']
    def __init__(self):
        self.sum = 0.0
        self.members = set()
    def addmember(self, member):
        self.members.add(member)
    def updatesum(self):
        self.sum = sum(member.output for member in self.members)
    def display(self):
        result = sorted(((unit.activation, unit.name) for unit in self.members), reverse=True)
        for i, (act, unitbyname) in enumerate(result):
            print '%s: %.2f\t' % (unitbyname, act),
            if i % 4 == 3: print
        print '\n'

def load(filename):
    """Load in a database and interpret it as a network

    First column must be unique keys which define the instance units.
    Each column is a pool (names, gangs, ages, etc).
    Every row is mutually excitory.
    """
    units[:] = []
    pools[:] = []
    for line in open(filename):
        relatedunits = line.split()
        if not len(relatedunits): continue
        key = len(units)
        for poolnum, name in enumerate(relatedunits):
            if poolnum >= len(pools):
                pools.append(Pool())
            pool = pools[poolnum]
            if name in unitbyname:
                unit = unitbyname[name]
            else:
                unit = Unit(name, pool)
                units.append(unit)
            pool.addmember(unit)
            if poolnum > 0:
                units[key].addexciter(unit)
                unit.addexciter(units[key])

def reset():
    for unit in units:
        unit.reset()

def depair(i, j):
    unitbyname[i].remove(unitbyname[j])
    unitbyname[j].remove(unitbyname[i])

def touch(itemstr, weight=1.0):
    for name in itemstr.split():
        unitbyname[name].setext(weight)

def run(times=100):
    """Run n-cycles and display result"""
    for i in xrange(times):
        for pool in pools:
            pool.updatesum()
        for unit in units:
            unit.computenewact()
        for unit in units:
            unit.commitnewact()
    print '-' * 20
    for pool in pools:
        pool.display()

if __name__ == '__main__' or 1:
    load('jets.txt')    
    touch('Ken', weight=0.8)
    run()

    reset()
    touch('Sharks 20 jh sing burglar')
    run()

    reset()
    touch('Lance')
    depair('Lance','burglar')
    run()

SampleFile = """
Art         Jets        40      jh      sing    pusher
Al          Jets        30      jh      mar     burglar
Sam         Jets        20      col     sing    bookie
Clyde       Jets        40      jh      sing    bookie
Mike        Jets        30      jh      sing    bookie
Jim         Jets        20      jh      div     burglar
Greg        Jets        20      hs      mar     pusher
John        Jets        20      jh      mar     burglar
Doug        Jets        30      hs      sing    bookie
Lance       Jets        20      jh      mar     burglar
George      Jets        20      jh      div     burglar
Pete        Jets        20      hs      sing    bookie
Fred        Jets        20      hs      sing    pusher
Gene        Jets        20      col     sing    pusher
Ralph       Jets        30      jh      sing    pusher

Phil        Sharks      30      col     mar     pusher
Ike         Sharks      30      jh      sing    bookie
Nick        Sharks      30      hs      sing    pusher
Don         Sharks      30      col     mar     burglar
Ned         Sharks      30      col     mar     bookie
Karl        Sharks      40      hs      mar     bookie
Ken         Sharks      20      hs      sing    burglar
Earl        Sharks      40      hs      mar     burglar
Rick        Sharks      30      hs      div     burglar
Ol          Sharks      30      col     mar     pusher
Neal        Sharks      30      hs      sing    bookie
Dave        Sharks      30      hs      div     pusher
"""
