import random
import copy
import time

def supersequence(x, y):
    """ True if and only if all elements in y occur in x in order (x is a supersequence of y)"""
    idx = 0
    try:
        for i in y:
            idx = x.index(i, idx)+1
    except ValueError, e:
        return False
    return True


def subsequence(x, y):
    """ x is a subsequence of y  <==>  y is a supersequence of x """
    return supersequence(y, x)


def is_supersequence_of_sequences(sequence, sequences):
    """ True if sequence is a supersequence of every s in sequences """
    result = True
    for s in sequences:
        if not supersequence(sequence, s):
            return False
    return result


def remove_redundant_sequences(redundant_sequences, debug=False):
    """ Removes every doublure sequence and every sequence that is a subsequence of another """
    if debug:
        print "Removing redundant sequences:"
    sequences = []
    for i,s in enumerate(redundant_sequences):
        remove = False
        for j in range(i+1, len(redundant_sequences)):
            if s == redundant_sequences[j]:
                remove = True
                if debug:
                    print "  Found doublure     ", s, "==", redundant_sequences[j]
        if not remove:
            sequences.append(s)
    sequences_p = []
    for i,s1 in enumerate(sequences):
        found = False
        for j,s2 in enumerate(sequences):
            if ((i != j) and (supersequence(s2, s1))):
                found = True
                if debug:
                    print "  Found supersequence", s2, "for", s1
                break
        if not found:
            sequences_p.append(s1)
    if debug:
        print "Removed %s redundant sequence(s). Reduced set:"%(len(redundant_sequences)-len(sequences_p))
        for i,s in enumerate(sequences_p):
            print " s%s:"%i, s
    return sequences_p


def lower_bound(scs):
    """ Finds a lower bound based on some fast algorithms."""
    def scs_length(s1, s2):
        """ shortest common supersequence length for two single sequences
            can be computed using dynamic programming. Based on algorithm for
            computing Longest Common Subsequence (== len(s1)+len(s2)-SCS )"""
        S = []
        for i in range(0, len(s1)+1):
            S.append([-1]*(len(s2)+1))
        for i in range(len(s1)+1):
            S[i][0] = i
        for j in range(len(s2)+1):
            S[0][j] = j
        for i in range(1, len(s1)+1):
            for j in range(1, len(s2)+1):
                if s1[i-1] == s2[j-1]:
                    S[i][j] = min(S[i-1][j]+1, S[i][j-1]+1, S[i-1][j-1]+1)
                else:
                    S[i][j] = min(S[i-1][j]+1, S[i][j-1]+1)
        return S[len(s1)][len(s2)]

    def find_max_scs_length_of_2_combinations(sequences):
        """ Returns maximum scs_length(s1,s2) for any s1, s2 in sequences. Note that this does not
            guarantee the length of the actual SCS of the entire set of sequences. """
        result = -1
        for i in range(len(sequences)):
            for j in range(i+1, len(sequences)):
                length = scs_length(sequences[i], sequences[j])
                if length > result:
                    result = length
        return result

    def max_count_occurrences(sequences):
        """ for every value v in the alphabet, for all s in sequences, count occurrences of v in s.
            The length of the SCS has be least the sum of maximum occurrences."""
        lower_bound = 0
        for v in set([s for seq in sequences for s in seq]):
            count_v = -1
            for s in sequences:
                count = s.count(v)
                if count > count_v:
                    count_v = count
            lower_bound += count_v
        return lower_bound

    return max(max_count_occurrences(scs), find_max_scs_length_of_2_combinations(scs))


def upper_bound(sequences, max_run_time_random_seconds = 1):
    """ Finds an upper bound based on some fast approximation algorithms."""

    def alphabet_leftmost(sequences):
        """ Approximation algorithm by looping through a random permutation on the alphabet """
        seqs = copy.deepcopy(sequences)
        common_supersequence = []
        permutation = list(set([x for s in seqs for x in s]))
        random.shuffle(permutation)
        i = 0
        while any(seqs):
            found = False
            for s in seqs:
                if s and s[0] == permutation[i]:
                    found = True
                    break
            if found:
                for s in seqs:
                    if s and s[0] == permutation[i]:
                        s.remove(permutation[i])
                common_supersequence.append(permutation[i])
            i = (i+1) % len(permutation)
        return common_supersequence


    def alphabet_leftmost_rand(sequences):
        """ Approximation algorithm using random selection on alphabet values. """
        seqs = copy.deepcopy(sequences)
        common_supersequence = []
        while any(seqs):
            firsts = list(set([s[0] for s in seqs if s]))
            next = firsts[random.randint(0, len(firsts)-1)]
            for s in seqs:
                if s and s[0] == next:
                    s.remove(next)
            common_supersequence.append(next)
        return common_supersequence

    def majority_merge(seqs):
        """ Quite fast approximation algorithm """
        sequences = copy.deepcopy(seqs)
        common_supersequence = []
        while any(sequences):
            firsts = [(s[0], len(s)) for s in sequences if s]
            counts = {}
            for x in firsts:
                if x[0] in counts:
                    counts[x[0]] += x[1]    #use +1 if not weighted MM
                else:
                    counts[x[0]] = x[1]     #use 1 if not weighted MM
            most_common = sorted(counts, key=lambda x: counts[x], reverse=True)[0]
            common_supersequence.append(most_common)
            for s in sequences:
                if s and s[0] == most_common:
                    s.remove(most_common)
                    if s == []:
                        sequences.remove([])
        return common_supersequence

    trivial = sum(len(s) for s in sequences)
    mm = len(majority_merge(sequences))
    alm, almr = 10000000, 10000000
    start = time.time()
    while time.time() < start + max_run_time_random_seconds:
        alm_test = alphabet_leftmost(sequences)
        if len(alm_test) < alm:
            alm = len(alm_test)
        almr_test = alphabet_leftmost_rand(sequences)
        if len(almr_test) < almr:
            almr = len(almr_test)
    upperbounds = [trivial, mm, alm, almr]
    solutions = bfs_genetic(sequences, keep_best = 1000, best_so_far = min(upperbounds))
    if solutions:
        upperbounds.append(sorted(solutions)[0])
    return min(upperbounds)


def backtrack_shortest_common_supersequences(sequences, upperbound=None):
    """ backtrack with pruning, then filter out the shortest SCSs (they are not unique!)"""
    if not upperbound:
        upperbound = 10000000
    result = backtrack_scs(sequences, [], upperbound)
    return [x for x in result if len(x) == min([len(y) for y in result])]

def backtrack_all_common_supersequences(sequences):
    """ backtrack all supersequences (not just shortest) """
    upperbound = 10000000
    return backtrack_scs(sequences, [], upperbound, False)

def backtrack_scs(sequences, choices, best_so_far, prune=True):
    """ Recursive DFS algorithm, potentially risky with large #sequences or long s in sequences"""
    solutions = []
    if any(sequences):
        # no need to evaluate subsolution choices if it will become longer than best_so_far.
        if not prune or len(choices) + max([len(s) for s in sequences]) <= best_so_far:
            firsts = set([s[0] for s in sequences if s])
            for c in firsts:
                indices = []
                for i,s in enumerate(sequences):
                    if s and s[0] == c:
                        s.remove(c)
                        indices.append(i)
                for solution in backtrack_scs(sequences, choices+[c], best_so_far):
                    solutions.append(solution)
                for i in indices:
                    sequences[i] = [c]+sequences[i]
    else:
        solutions = [choices]
        if len(choices) < best_so_far:
            best_so_far = len(choices)
    return solutions


def bfs_genetic(sequences, keep_best = 100000000, best_so_far = 100000000):
    """ Breath first search algorithm. Prunes away up to keep_best subsolutions according to metric() """
    def metric((choices, remaining_sequences)):
        # TODO: find good metric, given current choices and remaining sequences to solve.
        # return sum(len(s) for s in remaining_sequences)
        return len(remove_redundant_sequences(copy.deepcopy(remaining_sequences)))

    Q = []
    solutions = {}
    firsts = set([s[0] for s in sequences if s])
    for f in firsts:
        seqs = copy.deepcopy(sequences)
        for s in seqs:
            if s and s[0] == f:
                s.remove(f)
        Q.append(([f], seqs))
    depth = 1
    while Q:
        if depth < len(Q[0][0]):
            if len(Q) > keep_best:
                # print "Throwing away", len(Q) - keep_best, "out of", len(Q), "at depth", depth
                Q = sorted(Q, key=metric)[:keep_best]
            depth += 1
        else:
            choices, seqs = Q.pop(0)
            if len(choices) + max([len(s) for s in seqs]) <= best_so_far:
                if any(seqs):
                    firsts = set([s[0] for s in seqs if s])
                    for f in firsts:
                        sequences = copy.deepcopy(seqs)
                        for s in sequences:
                            if s and s[0] == f:
                                s.remove(f)
                        Q.append((choices[:]+[f], sequences))
                else:
                    if depth in solutions:
                        solutions[depth].append(choices[:])
                    else:
                        solutions[depth] = [choices[:]]
    return solutions


def pretty_print_scs_with_sequences(scs, sequences):
    print "SCS: " + "".join([str(s) for s in scs])
    for i,aseq in enumerate(sequences):
        seq = [-1]*len(scs)
        idx = 0
        for v in aseq:
            while scs.index(v, idx) > idx:
                idx += 1
            seq[idx] = v
            idx += 1
        print " s%s: "%i + "".join([str(s) for s in seq]).replace("-1", ".")


if __name__=="__main__":
    def run_SCS_algorithms(sequences):
        sequences = remove_redundant_sequences(sequences, debug=True)
        lowerbound, upperbound = lower_bound(sequences), upper_bound(sequences)
        print "Lowerbound on Shortest Common Supersequence:", lowerbound
        print "Upperbound on Shortest Common Supersequence:", upperbound
        solutions = backtrack_shortest_common_supersequences(sequences, upperbound)
        print "Backtrack found %s SCSs of optimal length %s."%(len(solutions), len(solutions[0]))
        print "E.g.", solutions[0], "is valid:", is_supersequence_of_sequences(solutions[0], sequences)
        pretty_print_scs_with_sequences(solutions[0], sequences)

    sequences_1 = [ [1,2,3],
                    [1,2,5],
                    [3,1,5,4],
                    [1,2,1,5],
                    [1,2,5]]

    sequences_2 = [ [1,2,1,2,3],    # "acacg"
                    [1,4,1,3,1],    # "ataga"
                    [2,1,2,3,4],    # "cacgt"
                    [3,4,1,1,4]]    # "ctaat"

    sequences_3 = [ [5,2,1,6,3,6,3,1],
                    [1,4,1,3,1,5,1,2],
                    [2,1,6,3,4,4,2,3],
                    [3,4,5,1,4,6,1,2]]

    sequences_4 = [ [5,1,3,5,2,6],
                    [1,5,2,1,3,2,3,1],
                    [5,1,3,5,2,1,6,2],
                    [3,5,1,6,2,4,6,1,2]]

    run_SCS_algorithms(sequences_4)
