# Makes the KD-Tree far fast lookup
def make_kd_tree(points, dim, i=0):
    if len(points) > 1:
        points.sort(key=lambda x: x[i])
        i = (i + 1) % dim
        half = len(points) >> 1
        return (
            make_kd_tree(points[: half], dim, i),
            make_kd_tree(points[half + 1:], dim, i),
            points[half])
    elif len(points) == 1:
        return (None, None, points[0])

# K nearest neighbors. The heap is a bounded priority queue.
def get_knn(kd_node, point, k, dim, dist_func, return_distances=False, i=0, heap=None):
    import heapq
    is_root = not heap
    if is_root:
        heap = []
    if kd_node:
        dist = dist_func(point, kd_node[2])
        dx = kd_node[2][i] - point[i]
        if len(heap) < k:
            heapq.heappush(heap, (-dist, kd_node[2]))
        elif dist < -heap[0][0]:
            heapq.heappushpop(heap, (-dist, kd_node[2]))
        i = (i + 1) % dim
        # Goes into the left branch, and then the right branch if needed
        get_knn(kd_node[dx < 0], point, k, dim,
                dist_func, return_distances, i, heap)
        # -heap[0][0] is the largest distance in the heap
        if dx * dx < -heap[0][0]:
            get_knn(kd_node[dx >= 0], point, k, dim,
                    dist_func, return_distances, i, heap)
    if is_root:
        neighbors = sorted((-h[0], h[1]) for h in heap)
        return neighbors if return_distances else [n[1] for n in neighbors]

# For the closest neighbor
def get_nearest(kd_node, point, dim, dist_func, return_distances=False, i=0, best=None):
    if kd_node:
        dist = dist_func(point, kd_node[2])
        dx = kd_node[2][i] - point[i]
        if not best:
            best = [dist, kd_node[2]]
        elif dist < best[0]:
            best[0], best[1] = dist, kd_node[2]
        i = (i + 1) % dim
        # Goes into the left branch, and then the right branch if needed
        get_nearest(
            kd_node[dx < 0], point, dim, dist_func, return_distances, i, best)
        if dx * dx < best[0]:
            get_nearest(
                kd_node[dx >= 0], point, dim, dist_func, return_distances, i, best)
    return best if return_distances else best[1]




""" Usage """

import random

def rand_point(dim):
    return [random.uniform(-1, 1) for d in range(dim)]

dim = 3  # 3 dimensions
points = [rand_point(dim) for x in range(5000)]  # 5k random points
kd_tree = make_kd_tree(points=points, dim=dim) # make the kd tree

# If you need labeled points, checkout my other recipe on adding attributes to python list
# https://code.activestate.com/recipes/users/4192908/

print get_knn(
    kd_node=kd_tree, 
    point=[0] * dim, 
    k=8, 
    dim=dim, 
    dist_func=lambda a, b: sum((a[i] - b[i]) ** 2 for i in xrange(dim))) # Euclidean distance

print

print get_nearest(
    kd_node=kd_tree,
    point=[0] * dim,
    dim=dim,
    dist_func=lambda a, b: sum((a[i] - b[i]) ** 2 for i in xrange(dim))) # Euclidean distance
