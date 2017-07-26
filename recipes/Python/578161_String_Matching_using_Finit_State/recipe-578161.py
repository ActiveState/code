"""
This module executes the string matching between a input sequence T and an
pattern P using a Finite State Machine.
The complexity for building the transition function is O(m^3 x |A|) where A is the
alphabet. Since the string matching function scan the input sequence only once,
the total complexity is O(n + m^3 x |A|)

@author Filippo Squillace
@version 1.0.0
@date 07/06/2012

"""

def string_matching_FSM(T, trans, m):
    """
    T: is the input sequence;
    trans: is the transition function that define the pattern P we need to look
    for;
    m: lenght of the pattern
    """
    s = 0
    for i,c in enumerate(T):
        s = trans[s][c]
        if s == m:
            return i-m+1

    return -1

import string as st
def transition_function(P):
    """
    The main principle on building the transition function is to think about
    the fact that every time we scan a new character from the input sequence
    the suffix should match with the prefix of the pattern. If that is not
    possible for every length of the suffix, the next state need to be the
    initial, otherwise the length of the suffix that matches properly will be
    exactly the next state.
    """
    alphabet = st.ascii_letters+st.punctuation+st.digits+st.whitespace
    m = len(P)
    trans = [{c:0 for c in alphabet} for i in range(m)]
    for s in range(m):
        for c in alphabet:
            k = min(m, s+1)
            while (P[:s]+c)[-k:] != P[:k]:
                k-=1

            trans[s][c]=k

    return trans



if __name__=='__main__':
    import unittest
    class StringMatchTestCase(unittest.TestCase):
        def setUp(self):
            # Table of (sequence,pattern,expected_result)
            self.pos_cases = [\
                    ('abcbbaanmdiababcdrttf','ababcd',11),
                    ('abcbbaanmdiabafweefabab','abab',19),
                    ('abcbbaanmdiasfo pfj=pewpfiojafaXre8abbafw_ eefabab','aXre8ab',30)
                    ]

            self.neg_cases = [\
                    ('abcbbaanmdiabcdrttf','ababcd',-1),
                    ('abcbbaanmdiabafweefaba','abab',-1),
                    ('abcbb_?aaFSRnmfew345sdhfhhuw.fad iabafweefaba','abab',-1)
                    ]

        def test_positive(self):
            for (T,P,er) in self.pos_cases:
                trans = transition_function(P)
                res = string_matching_FSM(T, trans, len(P))
                self.assertEqual(res, er)

        def test_negative(self):
            for (T,P,er) in self.neg_cases:
                trans = transition_function(P)
                res = string_matching_FSM(T, trans, len(P))
                self.assertEqual(res, er)

    unittest.main()
