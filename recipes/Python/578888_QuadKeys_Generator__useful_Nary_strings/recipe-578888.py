from itertools import product
import unittest

class QuadKeyGenerator:

    def __init__(self, width):
        self.width = width
        self.odometerValues = [0] * self.width  # max limit for each value on the odometer

    #--- odometer approach iterative ---
    def getNext(self):
        l = self.width-1
        i = 1
        while l >= 0 and i !=0:
            self.odometerValues[l] = ((self.odometerValues[l]+1) % self.width) # Odometer resets after reaching 3 to 0
            if self.odometerValues[l] == 0:
                i = 1
            else:
                i = 0
            l = l - 1

        if i != 0 and l < 0:
            return False
        return True

    def generateQuadKeys(self):
        while True:
            yield "".join(str(i) for i in self.odometerValues)
            if self.getNext() == False:
                break

    #--- recursive approach ---
    def generateQK(self, qk, level):
        if level == 0:
            yield qk
        else:
            for i in range(self.width): # QuadKey
                backUp = qk
                qk = qk + str(i)
                for g in self.generateQK(qk, level -1):
                    yield g
                qk = backUp

    #--- itertools approach ---
    def generateQKItertools(self):
        s = [x for x in range(self.width)]
        p = product(s, repeat=self.width)
        for qk in p:
            yield ''.join(map(str, qk))

class QuadKeyGeneratorTest(unittest.TestCase):
    def test_quadKeys_10(self):

        width = 4
        qkg = QuadKeyGenerator(width)

        nonIterGen = qkg.generateQuadKeys()
        recurGen = qkg.generateQK("", 4)
        iterGen = qkg.generateQKItertools()

        for x in range(width**4):
            nonIterQK = nonIterGen.next()
            recurQK = recurGen.next()
            iterQK = iterGen.next()

            self.assertTrue(nonIterQK == recurQK and recurQK == iterQK)


if __name__ == "__main__":
    unittest.main()
