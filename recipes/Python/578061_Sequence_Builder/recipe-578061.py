"""
    @author  Thomas Lehmann
    @file    sequenceBuilder.py
    @brief   generates sequences throughout different combinations of functions
"""
import sys
import itertools
import inspect
import re

class Sequence(object):
    """ represents a sequence and the used formula """
    def __init__(self, sequence, formula):
        """ storing one sequence and the relating formula """
        self.sequence = sequence
        self.formula  = formula
        self.hashCode = hash(tuple(self.sequence))

    def __eq__(self, other):
        """ required for unique elements in set container """
        return self.hashCode == other.hashCode

    def __lt__(self, other):
        """ required for sorting only """
        for a,b in zip(self.sequence, other.sequence):
            if a < b: return True
            if a > b: return False
        return False

    def __hash__(self):
        """ required for unique elements in set container """
        return self.hashCode

    def __repr__(self):
        return "%s - %s" % (self.sequence, self.formula)

class SequenceBuilder(object):
    def __init__(self):
        """ initializes for empty containers only """
        self.registeredFunctions = []
        self.sequences = set()

    def add(self, function):
        """ adds a function to the list of functions
            @param function is expected to be a lambda expression
        """
        self.registeredFunctions.append(function)

    def createSequences(self, fromPosition, toPosition):
        """ using the permutation of all functions to generate sequences
            @param fromPosition start position/index/value
            @param toPosition end position/index/value
        """
        self.sequences = set()
        for r in range(1,len(self.registeredFunctions)):
            for functions in itertools.permutations(self.registeredFunctions, r):
                position = fromPosition
                sequence = []
                while position <= toPosition:
                    value = position
                    for function in functions:
                        value = function(value)
                    sequence.append(value)
                    position += 1
                self.sequences.add(Sequence(sequence[0:], self.combineFunctions(functions)))

    def combineFunctions(self, functions):
        """ generates a combined formula as used for the calculation
            @param functions the list of individual functions (lambda code)
            @return the combined formula
            @note out of scope is the simplification (like: (x+1)+1 => x+2)
        """
        expression = ""
        for function in reversed(functions):
            match = re.match(".*\((?P<expression>lambda.*)\).*", inspect.getsource(function))
            if match:
                functionCode = match.group("expression")
                functionCode = functionCode[functionCode.find(":")+1:].strip()
                if not len(expression):
                    expression = functionCode
                else:
                    expression = expression.replace("x", "("+functionCode+")")
        return expression

def main():
    """ application entry point """
    print("Sequence builder v0.1")
    print("...Using Python %s" % sys.version.replace("\n", " - "))
    builder = SequenceBuilder()
    builder.add(lambda x: x-1)
    builder.add(lambda x: x-2)
    builder.add(lambda x: x+1)
    builder.add(lambda x: x+2)
    builder.add(lambda x: 2*x)
    builder.add(lambda x: x**2)
    builder.add(lambda x: (-1)**x)
    # takes a while...
    builder.createSequences(1, 20)
    print("...%d sequences found:" % len(builder.sequences))
    for sequence in sorted(builder.sequences):
        print(sequence)

if __name__ == "__main__":
    main()
