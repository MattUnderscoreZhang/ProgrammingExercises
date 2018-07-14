# Brute force.
from myFunctions import isprime,primes

def p(A,B):
    if isprime(int(str(A)+str(B))) and isprime(int(str(B)+str(A))):
        return True
    return False

# Tabulate whether the first 1000 primes are concatable with each other.
prime=primes(1002)
prime.pop(2)
prime.pop(0)
concatable=[[False]*1000]*1000
for i in range(1000):
    for j in range(i):
        concatable[j][i]=p(prime[i],prime[j])
        concatable[i][j]=p(prime[i],prime[j])
C=concatable
# For some reason the value of C[i][j] for i>j is unstable. Do not use.

minSum=10**6
for a in range(1000):
    for b in range(a):
        if C[b][a]:
            for c in range(b):
                if C[c][a] and C[c][b]:
                    for d in range(c):
                        if C[d][a] and C[d][b] and C[d][c]:
##                            newSum=prime[a]+prime[b]+prime[c]+prime[d]
##                            if newSum<minSum:
##                                minSum=newSum
##                                print prime[a]
##                                print prime[b]
##                                print prime[c]
##                                print prime[d]
##                                print minSum
                            for e in range(d):
                                if C[a][e] and C[b][e] and C[c][e] and C[d][e]:
                                    newSum=prime[a]+prime[b]+prime[c]+prime[d]+prime[e]
                                    if newSum<minSum:
                                        minSum=newSum
                                        print minSum
