# The number has to start with 1, because it does not increase in digits when
# multiplied by 6.

from itertools import permutations
from myFunctions import isprime

found=False
digits=2
while not found:
    for x in range(10**(digits-1),2*10**(digits-1)-1):
        orderedx=sorted(str(x))
        for i in range(2,7):
            if sorted(str(i*x))==orderedx:
                print x
                found=True
            else:
                found=False
                break
        if found:
            break
    digits+=1
