# Work your way up!

from myFunctions import *

# Does not apply to single-digit numbers.
def truncatablePrimeLeft(num):
    if int(num/10)==0:
        return isprime(num)
    elif not isprime(num):
        return False
    elif truncatablePrimeLeft(int(str(num)[1:])):
        return True
    return False

def truncatablePrimeRight(num):
    if int(num/10)==0:
        return isprime(num)
    elif not isprime(num):
        return False
    elif truncatablePrimeRight(int(num/10)):
        return True
    return False

# Add to left.
prospects=[2,3,5,7]
winners=[]
while prospects!=[]:
    prospect=prospects[0]
    for i in range(1,10):
        lefty=int(str(i)+str(prospect))
        if isprime(lefty):
            prospects.append(lefty)
    if truncatablePrimeRight(prospect) and prospect not in winners and prospect>9:
        winners.append(prospect)
    prospects.pop(0)
    if len(winners)==11:
        break

print winners
print sum(winners)
