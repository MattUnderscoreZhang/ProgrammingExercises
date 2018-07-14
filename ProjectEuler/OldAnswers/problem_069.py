# Matt Zhang
# Last Updated 2014-01-12
# Python 3.3.3

import numpy,random
from fractions import gcd

# Instead of figuring out how many numbers don't have any of the same factors as n, it's
# a lot easier to figure out how many numbers do share factors, and then to subtract
# them off.

# I had a prime factorizer somewhere, but I guess I'll just rip one from online since
# it's not with me. This is Pollard-Rho-Brent factorization. You put in an integer and
# it returns a random factor. Keep calling until finished.

def brent(N):
    if N%2==0:
        return 2
    y,c,m = random.randint(1, N-1),random.randint(1, N-1),random.randint(1, N-1)
    g,r,q = 1,1,1
    while g==1:             
        x = y
        for i in range(r):
            y = ((y*y)%N+c)%N
        k = 0
        while (k<r and g==1):
            ys = y
            for i in range(min(m,r-k)):
                y = ((y*y)%N+c)%N
                q = q*(abs(x-y))%N
            g = gcd(q,N)
            k = k + m
        r = r*2
    if g==N:
        while True:
            ys = ((ys*ys)%N+c)%N
            g = gcd(abs(x-ys),N)
            if g>1:
                break
    return g

# Ripped a prime checker too.

def is_prime(n):
    if n == 2 or n == 3: return True
    if n < 2 or n%2 == 0: return False
    if n < 9: return True
    if n%3 == 0: return False
    r = int(n**0.5)
    f = 5
    while f <= r:
        if n%f == 0: return False
        if n%(f+2) == 0: return False
        f +=6
    return True

# The program begins.

def factor(n):
    factors=[]
    while n!=1:
        newFactor=brent(n)
        n//=newFactor
        if is_prime(newFactor):
            factors.append(newFactor)
        else:
            factors+=(factor(newFactor))
    return factors

from collections import Counter
from itertools import combinations

# For integer n>1.
def totient(n):
    factors=Counter(factor(n))
    uniqueFactors=list(factors.keys())
    totient=n-1
    # Subtract multiples of each factor, then add back the ones you double-subtracted,
    # triple subtracted, etc.
    for uniqueFactor in uniqueFactors:
        totient-=(n-1)//uniqueFactor
    # Create every combination of factor products.
    combinationFactors=[]
    for i in range(2,len(uniqueFactors)):
        combinationFactors+=list(combinations(uniqueFactors,i))
    combinationFactors=[numpy.product(i) for i in combinationFactors]
    # Add them back in.
    for combinationFactor in combinationFactors:
        totient+=(n-1)//combinationFactor
    return totient

maxRatio=1
maxn=0

for n in range(2,1000000):
    print(n)
    ratio=n/totient(n)
    if ratio>maxRatio:
        maxRatio=ratio
        maxn=n

print(maxn)

# Ran real slow, but I don't want to do it over. Looking at it now, it was a bad idea
# to generate factors for each integer. It would have been better just to generate a
# list of primes and then to go through and label the numbers with their factors all at
# once. Probably would have sped up the program by a good 3 times.

# Gah, this isn't even correct. I'm listing numbers way greater than the original.
