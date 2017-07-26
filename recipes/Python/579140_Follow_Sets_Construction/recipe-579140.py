# Follow Sets Construction using prioritydictionary and graphs.
# Narayana Chikkam, Dec, 22, 2015.

import collections

from lib.graph import  *

class Grammar:
    prodNum = 0

    def __init__(self, sg):
        self.g = {}
        self.np = {}

        self.processStringsToGrammar(sg)

        self.sigma = self.orderSymbols()
        self.v = list(map(str, self.g.keys()))  # chg#1
        self.t = self.orderTerminals()
        self.prepareNullablesMap()
        self.numberedProds = None

    def processStringsToGrammar(self, sg):

        prods = sg.splitlines()
        if len(prods) > 0:
            self.g = collections.OrderedDict()
            self.np = collections.OrderedDict()

            S = prods[0].split("->")[0].strip()

            self.np[0] = ["%s#"%(S), [S]]    # Adding the start production S'
            index = 1

            for prod in prods:
                (lhs, rhs) = prod.split("->")
                if index not in self.np:
                    self.np[index] = [lhs.strip(), list(rhs.strip().split())]
                    index += 1

            for k in self.np:
                lhs, rhs = self.np[k][0], self.np[k][1]
                if lhs not in self.g:
                    self.g[lhs] = []
                self.g[lhs].append(rhs)


    def orderSymbols(self):
        symbols = []
        for k in self.g:  # order really matters
            if k not in symbols:
                symbols.append(k)
            for prods in self.g[k]:
                for s in prods:
                    if s not in symbols:
                        symbols.append(s)
        return symbols
        """
        ss = [prods for x in self.g.values() for prods in x]
        for prod in ss:
            symbols |= set(prod)
        return symbols
        """

    def orderTerminals(self):
        terminals = []
        for s in self.sigma:
            if s not in self.v:
                terminals.append(str(s))
        return terminals

    # NULLABLES CALCULATION:
    # can be optimized, recursion hits for limit 1000 default in Python!!!
    ######################################################################
    def isNullableRecursively(self, v):
        if self.visited[v] == False:
            self.visited[v] = True
            for prod in self.g[v]:
                #epsilonProd = ['epsilon']
                if 'epsilon' in prod: # Epsilon production
                    self.nullables_map[v] = True
                    break
                else:
                    prodNullableCount = 0
                    for prefix in prod:
                        if prefix in self.t:
                            break
                        if self.isNullableRecursively(prefix):
                            self.nullables_map[prefix] = True
                            prodNullableCount += 1
                        else:
                            break

                    if prodNullableCount == len(prod):
                        self.nullables_map[v] = True
                        break

            if v not in self.nullables_map:
                self.nullables_map[v] = False

            self.visited[v] = False
            return self.nullables_map[v]

    def prepareNullablesMap(self):
        self.visited = {k: False for k in self.v}
        self.nullables_map = {k: False for k in self.v}
        for v in self.v:
            self.nullables_map[v] = self.isNullableRecursively(v)


    def getNullablesMap(self):
        return self.nullables_map

    # FIRST CALCULATION:
    ######################################################################
    """
        find direct contributions and
        contains-the-FIRSTs-of
    """
    def findDirectFirstSets(self, v):
        first = set()
        for prod in self.g[v]:
            count = 0 # variable to check if this v could yeild epsilon because other pre-prefixes
            for prefix in prod:
                if prefix in self.t:
                    first = first.union([prefix])
                    break
                elif self.nullables_map[prefix] == True: # nullable V, go to next
                    self.containsFIRSTsOf.append((v, prefix))
                    count += 1
                    continue
                else:
                    self.containsFIRSTsOf.append((v, prefix))
                    break
            if count == len(prod):
                # all vars could produce nulls so add this v can indirectly produces epsilon
                first = first.union(['epsilon'])
        return first

    def getDirectFirstSets(self):
        self.init_first = {}
        self.containsFIRSTsOf = []
        for v in self.v:
            self.init_first[v] = self.findDirectFirstSets(v)

        return self.init_first

    def FIRST(self):

        initFirst = self.getDirectFirstSets()

        # create Graph withe the edges from containsOF relation
        g = Graph()
        for v in self.v:
            g.addVertex(v)

        for a,b in self.containsFIRSTsOf:
            g.addEdge(a, b, 1)

        #print "whole Graph: ", ffg
        return g.computeFirstUsingSCC(initFirst)

    # asking for first(rhs) of a particular production
    def FIRSTOFRHS(self, rhs):
        first = self.FIRST()
        retFirst = set()

        count = 0 # variable to check if this v could yeild epsilon because other pre-prefixes
        for prefix in rhs:
            if prefix in self.t:
                retFirst = retFirst.union([prefix])
                break
            elif self.nullables_map[prefix] == True: # nullable V, go to next
                retFirst = retFirst.union(first[prefix] - set(['epsilon']))
                count += 1
                continue
            else:
                retFirst = retFirst.union(first[prefix])
                break
        if count == len(rhs):
            # all vars could produce nulls so add this v can indirectly produces epsilon
            retFirst = retFirst.union(['epsilon'])

        return retFirst


    # FOLLOW CALCULATION:
    ######################################################################
    def getDirectFollowSets(self, FIRST):
        """
            1. If $ is the input end-marker, and S is the start symbol, $ belongs to FOLLOW(S).
            2. If there is a production, A -> Alpha B Beta, then FOLLOW(B) contains (FIRST(Beta) - epsilon)
            3. If there is a production, A -> Alpha B, or a production A -> Alpha B Beta, where  epsilon is in FIRST(Beta) , then FOLLOW(B) contains FOLLOW(A).
        """
        self.init_follow = {v:set() for v in self.v }
        self.containsFOLLOWOf = set()
        for v in self.v:
            if v == self.np[0][0]:  # Starting Production
                self.init_follow[v] = set(['$']) # $ is in follow of 'S' applying rule 1
            for prod in self.g[v]:
                for i in range(len(prod)):
                    if prod[i] in self.v and i+1 < len(prod):
                        if prod[i+1] in self.t:
                            self.init_follow[prod[i]] |= set([prod[i+1]])
                        else:
                            t = i + 1
                            while t < len(prod) and prod[t] in self.nullables_map:
                                if self.nullables_map[prod[t]] == True:
                                    self.init_follow[prod[i]] |= FIRST[prod[t]]-set(['epsilon'])
                                else:
                                    self.init_follow[prod[i]] |= FIRST[prod[t]]
                                    break
                                t += 1
                            if t >= len(prod): # every thing on rhs of prod[i] could produce epsison, rule - 3
                                self.containsFOLLOWOf |= set([(prod[i], v)])
                            else: #prod[i+1] is a non nullable prod or prod[t] was a terminal
                                if prod[t] in self.t:
                                    self.init_follow[prod[i]] |= set([prod[t]])
                                else:
                                    self.init_follow[prod[i]] |= FIRST[prod[t]]-set(['epsilon'])

                    elif prod[i] in self.v:
                        self.containsFOLLOWOf |= set([(prod[i], v)])         # applying rule 2

        #self.containsFOLLOWOf = set([(a, b) for (a, b) in self.containsFOLLOWOf if a != b]) # remove the self loops
        return self.init_follow

    def FOLLOW(self):

        first = self.FIRST()

        init_follow = self.getDirectFollowSets(first)  # populates the containsFOLLOWOf set for SCC

        g = Graph()
        for v in self.v:
            g.addVertex(v)

        for a,b in self.containsFOLLOWOf:
            g.addEdge(a, b, 1)  # dummy edge to keep the edges

        return g.computeFollowUsingSCC(first, init_follow)
