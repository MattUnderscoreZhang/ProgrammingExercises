from itertools import permutations
from myFunctions import isprime

def largestPandigitPrime():
    primes=[]
    for n in range(9,0,-1):
        pandigits=list(permutations([i for i in range(1,n+1)]))
        pandigits=[int(''.join([str(j) for j in pandigits[i]])) for i in range(len(pandigits))]
        for p in [2,3,5,7,11,13,17,19,23,29,31]:
            pandigits=[i for i in pandigits if i%p!=0]
        pandigits.sort(reverse=True)
        for i in range(len(pandigits)):
            if isprime(pandigits[i]):
                return pandigits[i]
    return 0

print largestPandigitPrime()
