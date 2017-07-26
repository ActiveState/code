from random import sample, randint

def isPrime(n):
    if n == 1:
        return 0
    else:
        for x in range(2, int(n ** 0.5) + 1):
            if n % x == 0:
                return 0
        return 1

isPrimeList = lambda n: [isPrime(i) for i in n]

def allPrimes(n, m):
    randBinList = lambda x: [randint(1, m) for b in range(1, x + 1)]
    parentA = randBinList(n)
    parentB = randBinList(n)
    while True:
        amount1 = randint(1, n)
        amount2 = randint(1, n)
        childA = sample(parentA, amount1)
        childA.extend(sample(parentB, n - amount1))
        childB = sample(parentA, amount2)
        childB.extend(sample(parentB, n - amount2))
        print(childA)
        print(childB)
        parentA = childA
        parentB = childB
        if all(isPrimeList(childA)) or all(isPrimeList(childB)):
            break
        elif any(isPrimeList(childA + childB)) == False:
            parentA = randBinList(n)
            parentB = randBinList(n)
