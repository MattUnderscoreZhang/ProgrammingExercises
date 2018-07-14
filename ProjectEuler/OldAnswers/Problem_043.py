from itertools import permutations
from myFunctions import isprime

pandigits=list(permutations([i for i in range(10)]))
pandigits=[int(''.join([str(j) for j in pandigits[i]])) for i in range(len(pandigits))]
primes=[2,3,5,7,11,13,17]
for n in range(2,9):
    pandigits=[i for i in pandigits if int(str(i)[n-1:n+2])%primes[n-2]==0]

print pandigits
print sum(pandigits)

# I don't know why it prints an 'L' on the ends of some numbers.
