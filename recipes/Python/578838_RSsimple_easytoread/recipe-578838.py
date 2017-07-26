"""Simple implementation of the RSA cryptosystem.

This module is meant to show a simple and clear implementation of the
RSA algorithm: http://en.wikipedia.org/wiki/RSA_(cryptosystem). It is meant
to be readable, not fast.

The usage is simple. First, create a random key pair:

    >>> public_key, private_key = make_key_pair(8)

The number 8 is the _key length_. The higher this number, the stronger the
encryption. The public key can be used to encrypt a message (in this module,
a message is simply a positive integer number):

    >>> message = 5
    >>> encrypted_message = public_key.encrypt(message)

The encrypted information can be retrieved only with the private key:

    >>> private_key.decrypt(encrypted_message)
    5

Private and public keys are made of three numeric parameters: ``n``, ``d`` and
``e``. ``n`` has the bit length specified with ``make_key_pair`` and is shared
between the two keys; ``e`` is used by the public key encrypt; ``d`` is used
by the private key to decrypt.

It's worth noting that ``n - 2`` is the highest number that can be safely
encrypted or decrypted. For example, encrypting (or decrypting) the number
``n - 1`` does nothing, and encrypting (or decrypting) the number ``n`` always
returns 0.

    >>> key = PublicKey(n=143, e=113)
    >>> key.encrypt(142)  # n - 1
    142
    >>> key.encrypt(143)  # n
    0

Also encrypting (or decrypting) 0 or 1 always returns 0 or 1:

    >>> key.encrypt(0)
    0
    >>> key.encrypt(1)
    1

Note that sometimes the original and the encrypted messages are the same, as
shown in the following example:

    >>> for x in range(143):  # n
    ...     if key.encrypt(x) == x:
    ...         print(x)
    0
    1
    12
    21
    34
    44
    65
    66
    77
    78
    99
    109
    122
    131
    142

"""

import random
from collections import namedtuple


def get_primes(start, stop):
    """Return a list of prime numbers in ``range(start, stop)``."""
    if start >= stop:
        return []

    primes = [2]

    for n in range(3, stop + 1, 2):
        for p in primes:
            if n % p == 0:
                break
        else:
            primes.append(n)

    while primes and primes[0] < start:
        del primes[0]

    return primes


def are_relatively_prime(a, b):
    """Return ``True`` if ``a`` and ``b`` are two relatively prime numbers.

    Two numbers are relatively prime if they share no common factors,
    i.e. there is no integer (except 1) that divides both.
    """
    for n in range(2, min(a, b) + 1):
        if a % n == b % n == 0:
            return False
    return True


def make_key_pair(length):
    """Create a public-private key pair.

    The key pair is generated from two random prime numbers. The argument
    ``length`` specifies the bit length of the number ``n`` shared between
    the two keys: the higher, the better.
    """
    if length < 4:
        raise ValueError('cannot generate a key of length less '
                         'than 4 (got {!r})'.format(length))

    # First step: find a number ``n`` which is the product of two prime
    # numbers (``p`` and ``q``). ``n`` must have the number of bits specified
    # by ``length``, therefore it must be in ``range(n_min, n_max + 1)``.
    n_min = 1 << (length - 1)
    n_max = (1 << length) - 1

    # The key is stronger if ``p`` and ``q`` have similar bit length. We
    # choose two prime numbers in ``range(start, stop)`` so that the
    # difference of bit lengths is at most 2.
    start = 1 << (length // 2 - 1)
    stop = 1 << (length // 2 + 1)
    primes = get_primes(start, stop)

    # Now that we have a list of prime number candidates, randomly select
    # two so that their product is in ``range(n_min, n_max + 1)``.
    while primes:
        p = random.choice(primes)
        primes.remove(p)
        q_candidates = [q for q in primes
                        if n_min <= p * q <= n_max]
        if q_candidates:
            q = random.choice(q_candidates)
            break
    else:
        raise AssertionError("cannot find 'p' and 'q' for a key of "
                             "length={!r}".format(length))

    # Second step: choose a number ``e`` lower than ``(p - 1) * (q - 1)``
    # which shares no factors with ``(p - 1) * (q - 1)``.
    stop = (p - 1) * (q - 1)
    for e in range(3, stop, 2):
        if are_relatively_prime(e, stop):
            break
    else:
        raise AssertionError("cannot find 'e' with p={!r} "
                             "and q={!r}".format(p, q))

    # Third step: find ``d`` such that ``(d * e - 1)`` is divisible by
    # ``(p - 1) * (q - 1)``.
    for d in range(3, stop, 2):
        if d * e % stop == 1:
            break
    else:
        raise AssertionError("cannot find 'd' with p={!r}, q={!r} "
                             "and e={!r}".format(p, q, e))

    # That's all. We can build and return the public and private keys.
    return PublicKey(p * q, e), PrivateKey(p * q, d)


class PublicKey(namedtuple('PublicKey', 'n e')):
    """Public key which can be used to encrypt data."""

    __slots__ = ()

    def encrypt(self, x):
        """Encrypt the number ``x``.

        The result is a number which can be decrypted only using the
        private key.
        """
        return pow(x, self.e, self.n)


class PrivateKey(namedtuple('PrivateKey', 'n d')):
    """Private key which can be used both to decrypt data."""

    __slots__ = ()

    def decrypt(self, x):
        """Decrypt the number ``x``.

        The argument ``x`` must be the result of the ``encrypt`` method of
        the public key.
        """
        return pow(x, self.d, self.n)


if __name__ == '__main__':
    # Test with known results.
    public = PublicKey(n=2534665157, e=7)
    private = PrivateKey(n=2534665157, d=1810402843)

    assert public.encrypt(123) == 2463995467
    assert public.encrypt(456) == 2022084991
    assert public.encrypt(123456) == 1299565302

    assert private.decrypt(2463995467) == 123
    assert private.decrypt(2022084991) == 456
    assert private.decrypt(1299565302) == 123456

    # Test with random values.
    for length in range(4, 17):
        public, private = make_key_pair(length)

        assert public.n == private.n
        assert len(bin(public.n)) - 2 == length

        x = random.randrange(public.n - 2)
        y = public.encrypt(x)
        assert private.decrypt(y) == x

        assert public.encrypt(public.n - 1) == public.n - 1
        assert public.encrypt(public.n) == 0

        assert private.decrypt(public.n - 1) == public.n - 1
        assert private.decrypt(public.n) == 0

    import doctest
    doctest.testfile(__file__, globs=globals())
