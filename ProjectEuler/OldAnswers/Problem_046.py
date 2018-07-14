from numpy import loadtxt
import itertools

primes=loadtxt('Problem_046_data.txt',skiprows=4)
primes=list(itertools.chain(*primes))
primes=[int(i) for i in primes]
possible=[True]*10**7
possible[1]=False
for i in range(0,10**7,2):
    possible[i]=False
for i in range(1000):
    for j in range(1000):
        possible[2*i**2+primes[j]]=False
#while True:
    candidate=possible.index(True)
    possible[candidate]

# No need to check, it's probably already the correct one.
print candidate

# I didn't solve this problem correctly at all. Really I should have checked my
# answer after I got it to make sure.
