from pickletools import genops

def optimize(p):
    'Optimize a pickle string by removing unused PUT opcodes'
    gets = set()            # set of args used by a GET opcode
    puts = []               # (arg, startpos, stoppos) for the PUT opcodes
    prevpos = None          # set to pos if previous opcode was a PUT
    for opcode, arg, pos in genops(p):
        if prevpos is not None:
            puts.append((prevarg, prevpos, pos))
            prevpos = None
        if 'PUT' in opcode.name:
            prevarg, prevpos = arg, pos
        elif 'GET' in opcode.name:
            gets.add(arg)

    # Copy the pickle string except for PUTS without a corresponding GET
    s = []
    i = 0
    for arg, start, stop in puts:
        j = stop if (arg in gets) else start
        s.append(p[i:j])
        i = stop
    s.append(p[i:])            
    return ''.join(s)


if __name__ == '__main__':
    from pickle import dumps
    from pickletools import dis

    p = dumps(['the', 'quick', 'brown', 'fox'])
    print 'Before:'
    dis(p)
    print '\nAfter:'
    dis(optimize(p))
