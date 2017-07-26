#! /usr/bin/env python
"""Compute a (somewhat more) human readable format for message
digests. This is port of the perl module Digest-BubbleBabble-0.01
(http://search.cpan.org/~btrott/Digest-BubbleBabble-0.01/)
"""

vowels = "aeiouy"
consonants = "bcdfghklmnprstvzx"


def bubblebabble(digest):
    """compute bubblebabble representation of digest.
    
    @param digest: raw string representation of digest (e.g. what md5.digest returns)
    @type digest: str

    @return: bubblebabble representation of digest
    @rtype: str
    """
    
    
    
    digest = [ord(x) for x in digest]
    
    dlen = len(digest)
    seed = 1
    rounds = 1+dlen/2
    retval = "x"
    for i in range(rounds):
	if i+1<rounds or dlen % 2:
	    idx0 = (((digest[2*i] >> 6) & 3) + seed) % 6
	    idx1 = (digest[2*i] >> 2) & 15;
            idx2 = ((digest[2*i] & 3) + seed / 6) % 6;
            retval += "%s%s%s" % (vowels[idx0], consonants[idx1], vowels[idx2])
	    if i+1 < rounds:
                idx3 = (digest[2 * i + 1] >> 4) & 15;
                idx4 = digest[2 * i + 1] & 15;
                retval += "%s-%s" % (consonants[idx3], consonants[idx4])
                seed = (seed * 5 + digest[2*i] * 7 +
                        digest[2*i+1]) % 36;
	else:
            idx0 = seed % 6;
            idx1 = 16;
            idx2 = seed / 6;
            retval += "%s%s%s" % (vowels[idx0], consonants[idx1], vowels[idx2])

    retval += "x"
    return retval

def hexstring2string(s):
    """convert hex representation of digest back to raw digest"""
    assert (len(s) % 2 == 0)
    if s.startswith("0x") or s.startswith("0X"):
	s = s[2:]
    return "".join([chr(eval("0x%s" % s[i:i+2])) for i in range(0, len(s), 2)])

def _test():
    tests = """432cc46b5c67c9adaabdcc6c69e23d6d xibod-sycik-rilak-lydap-tipur-tifyk-sipuv-dazok-tixox
5a1edbe07020525fd28cba1ea3b76694 xikic-vikyv-besed-begyh-zagim-sevic-vomer-lunon-gexex
1c453603cdc914c1f2eeb1abddae2e03 xelag-hatyb-fafes-nehys-cysyv-vasop-rylop-vorab-fuxux
df8ec33d78ae78280e10873f5e58d5ad xulom-vebyf-tevyp-vevid-mufic-bucef-zylyh-mehyp-tuxax
02b682a73739a9fb062370eaa8bcaec9 xebir-kybyp-latif-napoz-ricid-fusiv-popir-soras-nixyx"""
    # ...as computed by perl
    
    tests = [x.split()[:2] for x in tests.split("\n")]
    for digest, expected in tests:
	res=bubblebabble(hexstring2string(digest))
	print digest, res, ("failure", "ok")[expected==res]


if __name__=="__main__":
    _test()
