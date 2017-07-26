"""
A 'state tree' is (as its name implies) an object that represents a tree of
states.  The tree is built by having an initial state (the 'root') and a
rule whereby child states can be reached from a parent state.

State trees are useful, for example, in solving puzzles where there are a
fixed set of moves from any given position, and a goal position which is
the solution.  A couple of example puzzles are given below.
"""

from collections import deque


class StateTree(object):
    """
    Representation of a tree of states.

    States must be hashable (i.e., usable as dictionary keys---for example,
    tuples).  The initial(), reachable() and endcondtion() methods must be
    subclassed.  After that, the findpath() method will return a list of
    states from the initial to an end state.
    """

    def initial(self):
        "Return the initial state."
        raise NotImplementedError

    def reachable(self, state):
        "Yield states reachable from a given state."
        raise NotImplementedError

    def endcondition(self, state):
        "Return whether state satisfies the end condition."
        raise NotImplementedError

    def findpath(self):
        "Find and return shortest path from initial to end state."

        # Get the initial state.
        state = self.initial()

        # Mapping of state to its parent, or None if initial.
        parentmap = {state: None}

        # Queue of states to examine.
        queue = deque([state])

        # Process each state in the queue.
        while len(queue) > 0:
            state = queue.popleft()

            # Examine each new reachable state.
            for child in self.reachable(state):
                if child not in parentmap:
                    parentmap[child] = state
                    queue.append(child)

            # If this state satisfies the end condition, return it.
            if self.endcondition(state):
                states = [state]
                while parentmap[state] is not None:
                    state = parentmap[state]
                    states.insert(0, state)

                return states


class BottlePuzzle(StateTree):
    """
    There are three bottles, with capacities of 3, 5 and 8 litres.  You can
    pour the contents of one bottle into another until it's empty or the
    other is full.  How do you measure out 4 litres?
    """

    # Bottle sizes.
    sizes = (3, 5, 8)

    # Possible pourings (from -> to).
    pourings = ((0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1))

    def initial(self):
        return (0, 0, 8)

    def reachable(self, state):
        for a, b in self.pourings:
            bottles = list(state)

            # Get the amount poured from bottle A to bottle B.
            poured = min(self.sizes[b] - bottles[b], bottles[a])

            # If some was poured, yield the new state.
            if poured > 0:
                bottles[a] -= poured
                bottles[b] += poured
                yield tuple(bottles)

    def endcondition(self, state):
        return 4 in state


class FrogsAndToads(StateTree):
    """
    The classic frogs-and-toads puzzle.  An equal number of frogs and toads
    face each other on a log, with a gap between them, and need to swap
    places.  Toads only move right, frogs only move left.  A thing can move
    into the gap, or jump over a different thing into the gap.  How do they
    do it?
    """

    def initial(self):
        return ('T', 'T', 'T', ' ', 'F', 'F', 'F')

    def reachable(self, state):
        for thing, move in (('T', 1), ('T', 2), ('F', -1), ('F', -2)):
            pos = list(state)

            # Find where the empty space is.
            space = pos.index(' ')

            # Find start position of the thing to move.
            start = space - move

            # If start position is out of bounds, or not of the right type,
            # disallow it.
            if not 0 <= start < len(pos) or pos[start] != thing:
                continue

            # If it's a jump, and the jumped thing isn't a different kind,
            # disallow it.
            if abs(move) == 2 and pos[(space + start) / 2] == thing:
                continue

            # Do the move and yield it.
            pos[start], pos[space] = pos[space], pos[start]
            yield tuple(pos)

    def endcondition(self, state):
        return state == ('F', 'F', 'F', ' ', 'T', 'T', 'T')

if __name__ == "__main__":
    for puzzle in FrogsAndToads, BottlePuzzle:
        print
        print puzzle.__name__
        print
        for state in puzzle().findpath():
            print "   ", state
