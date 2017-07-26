def prime_numbers_less_than(N):
    if N <= 3:
        return range(2,N)

    primes = [2] +  range(3,N,2)

    index = 1
    max = N ** 0.5
    while 1:
        i = primes[index]
        if i>max:
            break
        index += 1
        primes = [x for x in primes if (x % i) or (x == i)]
    return primes
