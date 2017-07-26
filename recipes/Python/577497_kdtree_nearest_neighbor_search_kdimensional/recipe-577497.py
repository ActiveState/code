import collections
import itertools
import math

def square_distance(a, b):
    s = 0
    for x, y in itertools.izip(a, b):
        d = x - y
        s += d * d
    return s

Node = collections.namedtuple("Node", 'point axis label left right')

class KDTree(object):
    """A tree for nearest neighbor search in a k-dimensional space.

    For information about the implementation, see
    http://en.wikipedia.org/wiki/Kd-tree

    Usage:
    objects is an iterable of (point, label) tuples
    k is the number of dimensions
    
    t = KDTree(k, objects)
    point, label, distance = t.nearest_neighbor(destination)
    """

    def __init__(self, k, objects=[]):

        def build_tree(objects, axis=0):

            if not objects:
                return None

            objects.sort(key=lambda o: o[0][axis])
            median_idx = len(objects) // 2
            median_point, median_label = objects[median_idx]

            next_axis = (axis + 1) % k
            return Node(median_point, axis, median_label,
                        build_tree(objects[:median_idx], next_axis),
                        build_tree(objects[median_idx + 1:], next_axis))

        self.root = build_tree(list(objects))


    def nearest_neighbor(self, destination):

        best = [None, None, float('inf')]
        # state of search: best point found, its label,
        # lowest squared distance

        def recursive_search(here):

            if here is None:
                return
            point, axis, label, left, right = here

            here_sd = square_distance(point, destination)
            if here_sd < best[2]:
                best[:] = point, label, here_sd

            diff = destination[axis] - point[axis]
            close, away = (left, right) if diff <= 0 else (right, left)

            recursive_search(close)
            if diff ** 2 < best[2]:
                recursive_search(away)

        recursive_search(self.root)
        return best[0], best[1], math.sqrt(best[2])

if __name__ == '__main__':

    from random import random
    
    k = 5
    npoints = 1000
    lookups = 1000
    eps = 1e-8
    
    points = [(tuple(random() for _ in xrange(k)), i)
              for i in xrange(npoints)]

    tree = KDTree(k, points)

    for _ in xrange(lookups):
        
        destination = [random() for _ in xrange(k)]
        _, _, mindistance = tree.nearest_neighbor(destination)
        
        minsq = min(square_distance(p, destination) for p, _ in points)
        assert abs(math.sqrt(minsq) - mindistance) < eps
