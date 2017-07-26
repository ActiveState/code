import queue

grids = []

################################################################################

grids.append('''\
OOOOOOOOOOOO
OOO        O
OO         O
OO X       O
O   #  #   O
O          O
O          O
O   #  #   O
OO      X OO
OOX       OO
OO     X OOO
OOOOOOOOOOOO''')

grids.append('''\
OOOOOOOOOOOO
OOOOOOOOOOOO
OOOOOOOOOOOO
OOO      OOO
OO   ##   OO
OO  O  #  OO
OO        OO
OO   XX   OO
OOO      OOO
OOOOOOOOOOOO
OOOOOOOOOOOO
OOOOOOOOOOOO''')

grids.append('''\
OOOOOOOOOOOO
O          O
O          O
O  #    #  O
O          O
O          O
O          O
O          O
O X     #  O
O          O
O          O
OOOOOOOOOOOO''')

grids.append('''\
OOOOOOOOOOOO
O    O    OO
O       # OO
O         OO
O         OO
OOX      OOO
O         OO
O        #OO
O         OO
O    O   OOO
OOOOOOOOOOOO
OOOOOOOOOOOO''')

grids.append('''\
OOOOOOOOOOOO
O O      O O
O  #       O
O        # O
O       X  O
O          O
O          O
O  #       O
O       #  O
O          O
O          O
OOOOOOOOOOOO''')

grids.append('''\
OOOOOOOOOOOO
O          O
O   O   #  O
O         OO
O          O
O          O
O        X O
O          O
O        # O
O #        O
O          O
OOOOOOOOOOOO''')

################################################################################

def reader(grid):
    walls = set()
    blocks = set()
    targets = set()
    for y, line in enumerate(grid.split('\n')):
        for x, char in enumerate(line):
            if char == 'O':
                walls.add((y, x))
            elif char == '#':
                blocks.add((y, x))
            elif char == 'X':
                targets.add((y, x))
    return walls, blocks, targets

def worker(walls, blocks, targets):
    states = {frozenset(blocks)}
    jobs = queue.Queue()
    jobs.put((blocks, None))
    while not jobs.empty():
        job = jobs.get()
        # Pick a block to move.
        for block in job[0]:
            # Move up.
            offset = 1
            temp = (block[0] - offset, block[1])
            while temp not in walls and temp not in job[0]:
                offset += 1
                temp = (block[0] - offset, block[1])
            offset -= 1
            # Check for movement.
            if offset:
                copy = set(job[0])
                copy.remove(block)
                copy.add((block[0] - offset, block[1]))
                if copy not in states:
                    if targets.issubset(copy):
                        return (copy, job)
                    states.add(frozenset(copy))
                    jobs.put((copy, job))
            # Move down.
            offset = 1
            temp = (block[0] + offset, block[1])
            while temp not in walls and temp not in job[0]:
                offset += 1
                temp = (block[0] + offset, block[1])
            offset -= 1
            # Check for movement.
            if offset:
                copy = set(job[0])
                copy.remove(block)
                copy.add((block[0] + offset, block[1]))
                if copy not in states:
                    if targets.issubset(copy):
                        return (copy, job)
                    states.add(frozenset(copy))
                    jobs.put((copy, job))
            # Move left.
            offset = 1
            temp = (block[0], block[1] - offset)
            while temp not in walls and temp not in job[0]:
                offset += 1
                temp = (block[0], block[1] - offset)
            offset -= 1
            # Check for movement.
            if offset:
                copy = set(job[0])
                copy.remove(block)
                copy.add((block[0], block[1] - offset))
                if copy not in states:
                    if targets.issubset(copy):
                        return (copy, job)
                    states.add(frozenset(copy))
                    jobs.put((copy, job))
            # Move right.
            offset = 1
            temp = (block[0], block[1] + offset)
            while temp not in walls and temp not in job[0]:
                offset += 1
                temp = (block[0], block[1] + offset)
            offset -= 1
            # Check for movement.
            if offset:
                copy = set(job[0])
                copy.remove(block)
                copy.add((block[0], block[1] + offset))
                if copy not in states:
                    if targets.issubset(copy):
                        return (copy, job)
                    states.add(frozenset(copy))
                    jobs.put((copy, job))
    print(len(states), 'Unique States')
    print('No Solution Found!')
    return (blocks, None)

def opener(walls, answer, targets):
    if answer[1] is not None:
        opener(walls, answer[1], targets)
    print(render(walls, answer[0], targets))

def render(walls, blocks, targets):
    box = {}
    for y, x in walls:
        if y not in box:
            box[y] = {}
        box[y][x] = 'O'
    for y, x in targets:
        box[y][x] = 'X'
    for y, x in blocks:
        box[y][x] = '#'
    max_y = max(box)
    max_x = 0
    for y in box:
        max_x = max(max_x, max(box[y]))
    lines = []
    for y in range(max_y + 1):
        line = ''
        for x in range(max_x + 1):
            line += box[y].get(x, ' ')
        lines.append(line)
    return '\n'.join(lines)

################################################################################

if __name__ == '__main__':
    walls, blocks, targets = reader(grids[-1])
    answer = worker(walls, blocks, targets)
    opener(walls, answer, targets); input()
