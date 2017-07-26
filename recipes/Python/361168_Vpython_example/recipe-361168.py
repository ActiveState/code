"""Block moving robot arm simulation"""

import sys
from visual import box, label, color, rate
from Numeric import array

class Arm(object):
    """Represents the robot arm"""

    def __init__(self, stacks):
        """Pass the Stacks instance"""
        self.stacks = stacks

    def _getBlocks(self, a, b):
        """Pass two zero based numbers and get two
        block objects. All checking done, returns (None, None)
        if the indexes are wrong
        """
        if not (0 < a < self.stacks.blockCount): return None, None
        if not (0 < b < self.stacks.blockCount): return None, None
        a = self.stacks.blocks[a]
        b = self.stacks.blocks[b]
        if a.position == b.position: return None, None
        return a, b

    def moveOnto(self, a, b):
        """
        Move a onto b

        Where a and b are block numbers, puts block a onto block b
        after returning any blocks that are stacked on top of blocks
        a and b to their initial positions. 
        """
        # Get the actual block objects
        a, b = self._getBlocks(a, b)
        if not a: return # Ignore bad indexes
        # Return blocks ontop of a to original positions (in reverse order of course)
        a.removeBlocksFromAbove()
        # Return blocks ontop of b to original positions
        b.removeBlocksFromAbove()
        # Move block a on top of block b
        a.moveTo(b.position)

    def moveOver(self, a, b):
        """
        Move a over b

        Where a and b are block numbers, puts block a onto the top of the stack
        containing block b, after returning any blocks that are stacked on top
        of block a to their initial positions.
        """
        a, b = self._getBlocks(a, b)
        if not a: return # Ignore bad indexes
        # Move all blocks in a's stack to their original positions
        a.removeBlocksFromAbove()
        # Move a to the top of b's stack
        a.moveTo(b.position)

    def pileOnto(self, a, b):
        """
        Pile a onto b

        Where a and b are block numbers, moves the pile of blocks consisting of 
        block a, and any blocks that are stacked above block a, onto block b. 
        All blocks on top of block b are moved to their initial positions prior 
        to the pile taking place. The blocks stacked above block a retain their
        order when moved.
        """
        a, b = self._getBlocks(a, b)
        if not a: return # Ignore bad indexes
        # Remove the blocks on top of block b
        b.removeBlocksFromAbove()
        # Remove all the blocks on top of a and including onto b's stack
        blocksToMove = [a] + a.above
        for bl in blocksToMove:
            bl.moveTo(b.position)
        # All the below code would have reversed the order of the blocks
        ##blocks = a.stack[a.stack.index(a):]
        ##while blocks:
        ##    blocks.pop().moveTo(b.position)
        # Shorter loop for python 2.3
        ## [bl.moveTo(b.position) for bl in blocks[::-1]]
        # Or for python 2.4
        ## [bl.moveTo(b.position) for bl in reversed(blocks)]
        # Or even this, but not very readable:
        ##for block in a.stack[:a.stack.index(a):-1]:
        ##    block.moveTo(b.position)

    def pileOver(self, a, b):
        """
        Pile a over b

        Where a and b are block numbers, puts the pile of blocks consisting of 
        block a, and any blocks that are stacked above block a, onto the top of
        the stack containing block b. The blocks stacked above block a retain
        their original order when moved.
        """
        a, b = self._getBlocks(a, b)
        if not a: return # Ignore bad indexes
        # Remove all the blocks on top of a and including onto b's stack
        blocksToMove = [a] + a.above
        for bl in blocksToMove:
            bl.moveTo(b.position)

    def quit(self):
        """
        Quit

        Terminates manipulations in the block world. 
        """
        # Print the output
        stacks = self.stacks
        for i in range(stacks.blockCount):
            lst = ' '.join([str(bl.initialPosition) for bl in stacks[i]])
            print '%2d: %s' % (i, lst)


class Stacks(object):
    """Represents the stacks where all the blocks are"""

    def __init__(self, num):
        """Pass the number of stacks"""
        self.blockCount = num
        # Create our list of blocks. This will never change
        self.blocks = [VBlock(self, i) for i in range(num)]
        # Create a list of stacks. Each stack is represented by a list
        self._stacks = []
        for i in range(num):
            self._stacks.append([self.blocks[i]])

    def __getitem__(self, i):
        """Just enables people to access our stacks in an easy readonly way"""
        return self._stacks.__getitem__(i)


class Block(object):
    """Represents a block"""

    def __init__(self, stacks, position):
        """
        Pass a reference to the stacks object that holds all the blocks
        and the index of the initial stack of the block
        """
        self.stacks = stacks
        self.initialPosition = position
        self._position = position

    def moveTo(self, newPosition):
        """Simply puts the block on top of the stack numbered newPosition"""
        if newPosition == self._position: return
        stack = self.stacks[self._position]
        stack.remove(self)
        self._position = newPosition
        self.stacks[newPosition].append(self)

    def removeBlocksFromAbove(self):
        """Takes all the blocks from above us and puts them in their original positions
        In starting on the top of course"""
        above = self.above
        while above:
            block = above.pop()
            block.moveTo(block.initialPosition)
        # The below line is a compressed version of the above code
        ##for block in a.above[::-1]: block.moveTo(block.initialPosition)

    # Property Definitions

    # The stack property returns the actual stack of blocks that we're in
    def get_stack(self): return self.stacks[self._position]
    stack = property(get_stack)

    # Allows one to get and set the index of the stack that we're in
    def get_position(self): return self._position
    def set_position(self, newPosition): self.moveTo(newPosition)
    position = property(get_position, set_position)
    
    # Returns a list of the blocks that are above us in our stack
    def get_above(self):
        s = self.stack
        i = self.stack.index(self)
        return s[i+1:]
    above = property(get_above)

class VBlock(Block):

    def __init__(self, stacks, position):
        """
        Pass a reference to the stacks object that holds all the blocks
        and the index of the initial stack of the block
        """
        Block.__init__(self, stacks, position)
        self.box = box(pos=(position-(stacks.blockCount/2), 0, 0), size=(.9,.9,.9), color=color.blue)
        self.label = label(pos=array(self.box.pos) + array([0,0,1]), text=str(position), opacity=0, box=0, line=0)

    def moveTo(self, newPosition):
        """Simply puts the block on top of the stack numbered newPosition"""
        Block.moveTo(self, newPosition)
        # Now animate our movement
        height = 0
        for block in self.stack:
            if block is self: break
            else: height -= 1
        start = array(self.box.pos)
        end = array((newPosition-(self.stacks.blockCount/2), height, 0))
        # Move in 30 steps
        step = array((end - start) / 30.)
        for i in range(1,31):
            self.box.pos = start + (step * i)
            self.label.pos = start + (step * i) + array([0,0,1])
            rate(120)
        self.box.pos = end
        self.label.pos = end + array([0,0,1])
        print self.box.pos

def parse():
    """Parses the user input, starting with the number of blocks"""
    # Get the number of blocks
    while 1:
        num = sys.stdin.readline()
        try:
            num = int(num[:-1])
        except Exception, e:
            if num.lower() == 'quit\n': return
            else: continue
        else: break
    # Create the objects
    stacks = Stacks(num)
    arm = Arm(stacks)
    # Now parse each line of input ignoring dumb commands
    while 1:
        line = sys.stdin.readline().lower()[:-1] # Remove the enter at the end and convert to lowercase
        if line == 'quit':
            arm.quit()
            break
        else:
            words = line.split()
            if len(words) != 4: continue
            if words[0] not in ('move', 'pile'): continue
            try:
                a = int(words[1])
                b = int(words[3])
            except:
                continue
            if words[2] not in ('onto', 'over'): continue
            command = words[0] + words[2].capitalize()
            func = getattr(arm, command)
            func(a,b)

def test1():
    s = RealStacks(10)
    a = Arm(s)
    a.moveOnto(9, 1)
    a.moveOver(8, 1)
    a.moveOver(7, 1)
    a.moveOver(6, 1)
    a.pileOver(8, 6)
    a.pileOver(8, 5)
    a.moveOver(2, 1)
    a.moveOver(4, 9)
    a.quit()

def test2():
    from StringIO import StringIO
    oldStdin = sys.stdin
    testInput = '\n'.join([
        '10',
        'move 9 onto 1',
        'move 8 over 1',
        'move 7 over 1',
        'move 6 over 1',
        'pile 8 over 6',
        'pile 8 over 5',
        'move 2 over 1',
        'move 4 over 9',
        'pile 9 onto 7',
        'pile 9 onto 1',
        'quit',
        ''])
    sys.stdin = StringIO(testInput)
    oldStdout = sys.stdout
    sys.stdout = s = StringIO()
    parse()
    sys.stdin = oldStdin
    sys.stdout = oldStdout
    reqd = '\n'.join([
        ' 0: 0',
        ' 1: 1 9 2 4',
        ' 2: ',
        ' 3: 3',
        ' 4: ',
        ' 5: 5 8 7 6',
        ' 6: ',
        ' 7: ',
        ' 8: ',
        ' 9: ',
        ''])
    s = s.getvalue()
    if s != reqd:
        print repr(s)
        print repr(reqd)
    else:
        print 'OK'
    sys.exit()

if __name__ == '__main__':
    test2()
