"Graph the progression towards Kaprekar's constant"

from collections import Counter

def step_function(n):
    'Do a single step in the Kaprekar process'
    # http://en.wikipedia.org/wiki/6174_(number)
    s = format(n, '04d')        # 1253          --> '1253'
    t = ''.join(sorted(s))      # '1253'        --> '1235'
    u = t[::-1]                 # '1235'        --> '5321'
    return int(u) - int(t)      # (5321 - 1235) --> 4086

main_template = '''
digraph kaprekar {
    rankdir=LR;
%s
%s
}
'''
node_template = '    "%s" [label="%s: %04d"];\n'
pair_template = '    "%s" -> "%s";\n'

def make_graph(show_counts=True):
    'Generate a dot file'
    # python analyze_6174.py | dot -Tpng > a6174.png && open a6174.png

    step = {i: step_function(i) for i in range(10000)}
    outs = Counter(step.values())  # only show destination nodes
    nodes = []
    if show_counts:
        nodes = [node_template % (i, c, i) for i, c in outs.items()]
    results = results = [pair_template % (i, step[i]) for i in outs]
    return main_template % (''.join(nodes), ''.join(results))

if __name__ == '__main__':
    print make_graph(show_counts=True)
