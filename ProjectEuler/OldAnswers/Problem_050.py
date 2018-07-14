from myFunctions import primes,isprime

prime=primes(10000)
sum=0
maxLength=0
while sum<=10**6:
    sum+=prime[maxLength]
    maxLength+=1

found=False
for runLength in range(maxLength-1,0,-1):
    for i in range(maxLength-runLength):
        sum=0
        for j in range(i,i+runLength):
            sum+=prime[j]
        if isprime(sum):
            print sum
            found=True
            break
    if found:
        break
