# Matt Zhang
# Last Updated 2014-01-12
# Python 3.3.3

# The ascending order doesn't matter at all here. You just need to know, for each
# denominator, how many other numbers don't share a factor with it. Same process as 69,
# but since I did 69 in a bad way, I'll start over here.

# Generate a list of unique prime factors.

prime=[True]*1000001
prime[0]=prime[1]=False
uniqueFactors=[[] for i in range(1000001)]
uniqueFactors[2].append(2)
for n in range(4,1000001,2):
    prime[n]=False
    uniqueFactors[n].append(2)
for p in range(3,1000001,2):
    if prime[p]:
        uniqueFactors[p].append(p)
        for n in range(2*p,1000001,p):
            prime[n]=False
            uniqueFactors[n].append(p)

# For integer n>1.

from itertools import combinations
from numpy import product

'''def totient(n):
    totient=n-1
    # Subtract multiples of each factor, then add back the ones you double-subtracted,
    # triple subtracted, etc.
    for uniqueFactor in uniqueFactors[n]:
        totient-=(n-1)//uniqueFactor
    # Create every combination of factor products.
    combinationFactors=[]
    for i in range(2,len(uniqueFactors[n])):
        combinationFactors+=list(combinations(uniqueFactors[n],i))
    combinationFactors=[product(i) for i in combinationFactors]
    # Add them back in.
    for combinationFactor in combinationFactors:
        totient+=(n-1)//combinationFactor
    return totient'''

def totient(n):
    totient=0
    for i in range(1,n):
        if #uniqueFactos[n] and uniqueFactors[i] have no elements in common:
            totient+=1
    return totient

# Count reduced proper fractions.

reduced=0

for i in range(2,1000001):
    reduced+=totient(i)
    print(i)

print(reduced)
