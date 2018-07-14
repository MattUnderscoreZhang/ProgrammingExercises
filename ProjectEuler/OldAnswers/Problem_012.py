# Tn, the nth triangle number, is equal to n(1+n)/2. The number of divisors
# a number has is easily calculated from its factors. If a number is equal
# to (2^5)*(3^6)*(5^2)*7, then the number of divisors is 6*7*3*2. Thus we
# see that the smallest triangle number to have over 500 divisors must skip
# no primes in its factorization.

def divisors(num):
    factors=prime_factors(num)
    product=1
    for i in range(0,len(factors)/2):
        product*=factors[2*i+1]+1
    return product

def prime_factors(num):
    factors=[]
    div=2
    while num>1:
        factors.append(div)
        factors.append(0)
        i=1
        while num%div==0:
            factors.pop()
            factors.append(i)
            i+=1
            num/=div
        div=div+1
    return factors

# n and n+1 share no prime divisors, so Tn has D(n)*D((n+1)/2) divisors, where
# D(n) is the number of divisors of n. So we just have to find the first number
# with ceiling(sqrt(500)) divisors, then start searching from there.

n=1
while True:
    div=divisors(n)
    if div>23:
        break
    else:
        n+=1

n=2*n-1
while True:
    div=divisors(n*(1+n)/2)
    if div>500:
        break
    else:
        n+=1

print n*(1+n)/2

# I don't feel like this solution was too good.
